import os
import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QLabel, QMessageBox, QDialog, QApplication, QDesktopWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.uic import loadUi
import numpy as np
import cv2
import time
import math
import datetime
import pyautogui
import matplotlib.pyplot as plt
from eyeGestures.utils import VideoCapture
from eyeGestures import EyeGestures_v3, EyeGestures_v2
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl

TC_IMAGE_DIRECTORY = "../../dataset/Images/TCImages"
TS_IMAGE_DIRECTORY = "../../dataset/Images/TSImages"

class ImagePopup(QDialog):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Viewer")

        layout = QVBoxLayout()

        # Load and display the image
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            QMessageBox.critical(self, "Error", f"Failed to load image: {image_path}")
            self.close()
        else:
            self.image_label.setPixmap(pixmap.scaled(640, 480, aspectRatioMode=1))  # Resize image
            layout.addWidget(self.image_label)

        self.setLayout(layout)


class DiagnosisScreen(QWidget):
    """Displays two tables with images from TCImages and TSImages directories."""
    def __init__(self, stacked_widget, model):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.model = model  

        loadUi('diagnosis.ui', self)

        self.image_drop_label = ImageDropLabel(model=self.model, parent_screen=self)

        self.diagnosis_label.setAlignment(Qt.AlignCenter)
        self.diagnosis_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.tc_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.ts_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        main_layout = QVBoxLayout(self)

        #main_layout.addWidget(self.image_drop_label)  # Optional: add to UI if needed

        self.search_bar.textChanged.connect(self.filter_images)
        self.diagnosis_button.clicked.connect(self.image_drop_label.gaze_tracker)
        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        self.setup_table(self.tc_table, "TC Images")
        self.setup_table(self.ts_table, "TS Images")

        self.tc_table.cellDoubleClicked.connect(lambda row, col: self.open_image_popup(row, col, TC_IMAGE_DIRECTORY, self.tc_table))
        self.ts_table.cellDoubleClicked.connect(lambda row, col: self.open_image_popup(row, col, TS_IMAGE_DIRECTORY, self.ts_table))

        self.setLayout(main_layout)

        self.load_images()


    def setup_table(self, table, title):
        """Configures the table settings."""
        table.setColumnCount(1)
        #table.setHorizontalHeaderLabels([title])
        # table.setColumnWidth(0, 300)

    def load_images(self):
        """Loads images from both directories into tables."""
        self.tc_images = self.get_image_list(TC_IMAGE_DIRECTORY)
        self.ts_images = self.get_image_list(TS_IMAGE_DIRECTORY)

        self.populate_table(self.tc_table, self.tc_images)
        self.populate_table(self.ts_table, self.ts_images)


    def get_image_list(self, directory):
        """Returns a list of image files from a directory."""
        if not os.path.exists(directory):
            QMessageBox.critical(self, "Error", f"Directory not found: {directory}")
            return []
        return [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    def populate_table(self, table, image_list):
        """Fills a table with provided image names."""
        table.setRowCount(len(image_list))
        for row, image_name in enumerate(image_list):
            table.setItem(row, 0, QTableWidgetItem(image_name))

    def open_image_popup(self, row, column, directory, table):
        """Opens a popup to display the selected image."""
        image_name = table.item(row, column).text()
        image_path = os.path.join(directory, image_name)

        self.image_popup = ImagePopup(image_path)
        self.image_popup.exec_()

    def filter_images(self):
        """Filters images based on search query for both tables."""
        query = self.search_bar.text().lower()

        filtered_tc_images = [img for img in self.tc_images if query in img.lower()]
        filtered_ts_images = [img for img in self.ts_images if query in img.lower()]

        self.populate_table(self.tc_table, filtered_tc_images)
        self.populate_table(self.ts_table, filtered_ts_images)

    def show_camera(self):
        self.camera_popup = CameraPopup()
        self.camera_popup.exec_()


class ImageDropLabel(QLabel):
    def __init__(self, model, parent_screen=None,height=200, width=150):
        super().__init__()
        self.setText("Drag and Drop an Image Here")
        self.setAlignment(Qt.AlignCenter)
        self.setMaximumSize(width, height)
        #self.move(600,200)
        self.setStyleSheet("border: 1px dashed #aaa; font-size: 16px; padding: 20px;")
        self.setAcceptDrops(True)
        self.model = model  # Load the ML model
        self.parent_screen = parent_screen

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.setPixmap(QPixmap(file_path).scaled(300, 300, Qt.KeepAspectRatio))

            # Process & Predict
            result = self.predict_image(file_path)
            if result==0:
                self.setText(f"Prediction: NON-ASD")  # Display result
            elif result==1:
                self.setText(f"Prediction: ASD")  # Display result
            else:
                self.setText(f"Diagnosis error!")  # Display result

    def predict_image(self, img):
        """ run prediction """

        prediction = self.model.predict(img)
        return np.argmax(prediction)  # Return predicted class index
    
    def average_laplacian(self,image):
        """Applies an average filter followed by a Laplacian filter."""
        kernel_size = (3, 3)  # Define kernel size for averaging
        average_filtered = cv2.blur(image, kernel_size)

        # Convert image to float64 for Laplacian
        image = image.astype(np.float64)  # Use np.float64 for the Laplacian filter

        # Apply the Laplacian filter
        laplacian_filtered = cv2.Laplacian(image, cv2.CV_64F)

        # Enhance the image
        enhanced_image = laplacian_filtered - average_filtered

        # Convert back to uint8 (clip to valid range)
        enhanced_image = np.clip(enhanced_image, 0, 255).astype(np.uint8)

        return enhanced_image

    def preprocess_image(self,img_array, color, target_size):
        """
        Preprocess a batch of images:
        - Convert each image in the batch to grayscale.
        - Resize each image to the target size.
        Args:
            img_array (np.array): Input batch of images (batch_size, H, W, C).
            target_size (tuple): Desired target size (width, height).
        Returns:
            np.array: Preprocessed grayscale images of target size (batch_size, H', W').
        """
        if img_array is None or img_array.size == 0:
            raise ValueError("Input image array is empty or None.")

        # Ensure the input image has the correct shape (single-channel grayscale)
        # if img_array.ndim == 3 and img_array.shape[-1] != 1:
        #     img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)  # Convert to grayscale if not already

        # Apply thresholding to create a binary image (make sure it's uint8)
        laplacian_img = cv2.threshold(img_array, 4, 255, cv2.THRESH_BINARY)[1]
        
        # Convert to uint8 explicitly (ensures the correct data type for processing)
        laplacian_img = np.uint8(laplacian_img)

        if color is False:
            # Apply histogram equalization (this requires an 8-bit single-channel image)
            grayscale_img = cv2.equalizeHist(laplacian_img)

            # Resize the image to the target size
            resized_img = cv2.resize(grayscale_img, target_size, interpolation=cv2.INTER_AREA)
            #resized_img = grayscale_img

            # Ensure the image has a single channel
            resized_img = np.expand_dims(resized_img, axis=-1)
        else:
            # If color processing is required, just resize the laplacian image
            #resized_img = laplacian_img
            resized_img = cv2.resize(laplacian_img, target_size, interpolation=cv2.INTER_AREA)

        return resized_img

    def gaze_tracker(self):
        self.popup = VideoPopup("asdd.mp4")
        self.popup.videoFinished.connect(self.finish_experiment)
        self.popup.finished.connect(self.cleanup_camera)

        diagnosis_screen = self.parentWidget().parentWidget()  # Traverse up to DiagnosisScreen
        if hasattr(diagnosis_screen, 'show_camera'):
            diagnosis_screen.show_camera()

        self.gestures = EyeGestures_v2()
        self.cap = VideoCapture(0)
        calibrate = True
        screen_width, screen_height = pyautogui.size()

        # Improved calibration: avoid corners
        x = np.linspace(0.2, 0.8, 4)
        y = np.linspace(0.2, 0.8, 4)
        xx, yy = np.meshgrid(x, y)
        calibration_map = np.column_stack([xx.ravel(), yy.ravel()])
        np.random.shuffle(calibration_map)

        self.gestures.uploadCalibrationMap(calibration_map, context="my_context")
        self.gestures.setFixation(1.0)

        self.scanpath_img = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
        self.prev_point = None
        self.distances = []
        self.start_time = time.time()
        self.duration = 100
        self.kalman = self.init_kalman_filter()
        
        self.popup.show()

        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(lambda: self.process_frame(screen_width, screen_height, calibrate))
        self.frame_timer.start(100)  # 10 FPS


    def init_kalman_filter(self):
        kalman = cv2.KalmanFilter(4, 2)
        kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                            [0, 1, 0, 0]], np.float32)
        kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                            [0, 1, 0, 1],
                                            [0, 0, 1, 0],
                                            [0, 0, 0, 1]], np.float32)
        kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03
        kalman.statePre = np.zeros((4, 1), dtype=np.float32)
        return kalman


    def process_frame(self, screen_width, screen_height, calibrate):
        if time.time() - self.start_time > self.duration:
            self.frame_timer.stop()
            return

        ret, frame = self.cap.read()
        if not ret or frame is None:
            QMessageBox.warning(self, "Tracking Error", "Face or eyes not detected. Please try again.")
            self.frame_timer.stop()
            self.cap.close()
            self.gaze_tracker()
            return

        try:
            event, cevent = self.gestures.step(frame, calibrate, screen_width, screen_height, context="my_context")
            if event:
                if int(event.point[0]) != 0 and int(event.point[1]) != 0:
                    current_point = (int(event.point[0]), int(event.point[1]))

                    # Kalman filter smoothing
                    measurement = np.array([[np.float32(current_point[0])],
                                            [np.float32(current_point[1])]])
                    self.kalman.correct(measurement)
                    predicted = self.kalman.predict()
                    smoothed_point = (int(predicted[0]), int(predicted[1]))

                    # Only draw line if movement is stable and not too fast (fixation threshold)
                    if self.prev_point is not None:
                        dist = math.dist(self.prev_point, smoothed_point)
                        velocity = dist / 0.1  # Approximate velocity (distance per 100ms)
                        #print(f"Distance: {dist:.2f}, Velocity: {velocity:.2f}")
                        if velocity < 600:  # Only draw for fixation-like movement
                            self.distances.append(dist)
                            cv2.line(self.scanpath_img, self.prev_point, smoothed_point,
                                    color=(255, 255, 255), thickness=2)

                    self.prev_point = smoothed_point

        except Exception as e:
            QMessageBox.warning(self, "Tracking Error", f"Error: {e}\nRestarting...")
            self.frame_timer.stop()
            self.cap.close()
            self.gaze_tracker()



    def finish_experiment(self):
        self.frame_timer.stop()
        self.popup.close()
        self.cap.close()

        processed_image = self.preprocess_image(self.scanpath_img, color=True, target_size=(224, 224))
        processed_image = np.expand_dims(processed_image, axis=0)

        if processed_image is None or processed_image.size == 0:
            QMessageBox.critical(self, "Error", "Processed image is empty.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"scanpath_{timestamp}.png"
        image_to_save = np.squeeze(processed_image, axis=0)
        cv2.imwrite(filename, image_to_save)

        result = self.predict_image(processed_image)
        resultTxt = "Non-ASD" if result == 0 else "ASD" if result == 1 else "Error"
        QMessageBox.information(self, "Diagnosis", resultTxt)

    def cleanup_camera(self):
        if hasattr(self, 'frame_timer') and self.frame_timer.isActive():
            self.frame_timer.stop()
        
        self.cap.close()
    
class CameraPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Camera")
        self.setFixedSize(640, 480)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        # Detect available screens
        app = QApplication.instance()
        screens = app.screens()
        print(screens)

        if len(screens) > 1:
            second_screen = screens[1]
            geometry = second_screen.geometry()
            self.move(geometry.x(), geometry.y())
            #self.showFullScreen()
        else:
            # Center on primary screen if only one
            screen = QDesktopWidget().screenGeometry()
            self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

        self.cap = cv2.VideoCapture(0)  # Open default camera (index 0)

        if not self.cap.isOpened():
            QMessageBox.critical(self, "Error", "Could not open the camera.")
            self.close()
            return

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Refresh every 30 ms


from PyQt5.QtCore import pyqtSignal

class VideoPopup(QDialog):
    videoFinished = pyqtSignal()

    def __init__(self, video_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Video Player")
        self.setMinimumSize(640, 480)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.media_player.mediaStatusChanged.connect(self.check_video_status)

        self.showFullScreen()

        self.media_player.play()

    def check_video_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.videoFinished.emit()