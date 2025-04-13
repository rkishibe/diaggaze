import os
import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QLabel, QMessageBox, QDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.uic import loadUi
import numpy as np

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
        loadUi('diagnosis.ui', self)

        self.diagnosis_label.setAlignment(Qt.AlignCenter)
        self.diagnosis_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.tc_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.ts_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        main_layout = QVBoxLayout(self)

        self.search_bar.textChanged.connect(self.filter_images)

        self.diagnosis_button.clicked.connect(self.show_camera)
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
    def __init__(self, model, height=200, width=150):
        super().__init__()
        self.setText("Drag and Drop an Image Here")
        self.setAlignment(Qt.AlignCenter)
        self.setMaximumSize(width, height)
        #self.move(600,200)
        self.setStyleSheet("border: 1px dashed #aaa; font-size: 16px; padding: 20px;")
        self.setAcceptDrops(True)
        self.model = model  # Load the ML model

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

    def predict_image(self, file_path):
        """ Convert image to tensor & run prediction """
        img = QImage(file_path)
        img = img.scaled(224, 224, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Resize to keep aspect ratio

        # Convert QImage to NumPy array
        img = img.convertToFormat(QImage.Format_RGB888)
        width, height = img.width(), img.height()
        ptr = img.bits()
        ptr.setsize(height * width * 3)
        img_array = np.frombuffer(ptr, np.uint8).reshape((height, width, 3))

        # Resize to 224x224 by padding if necessary
        if img_array.shape[0] < 224 or img_array.shape[1] < 224:
            # Create a 224x224 black background image
            padded_img = np.zeros((224, 224, 3), dtype=np.uint8)
            
            # Calculate the padding offsets for the center
            pad_top = (224 - img_array.shape[0]) // 2
            pad_bottom = 224 - img_array.shape[0] - pad_top
            pad_left = (224 - img_array.shape[1]) // 2
            pad_right = 224 - img_array.shape[1] - pad_left

            # Place the image in the center of the padding
            padded_img[pad_top:pad_top + img_array.shape[0], pad_left:pad_left + img_array.shape[1]] = img_array
            img_array = padded_img

        # Normalize and reshape
        #img_array = img_array.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Predict using ML model
        prediction = self.model.predict(img_array)
        return np.argmax(prediction)  # Return predicted class index
    
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

        self.cap = cv2.VideoCapture(0)  # Open default camera (index 0)

        if not self.cap.isOpened():
            QMessageBox.critical(self, "Error", "Could not open the camera.")
            self.close()
            return

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Refresh every 30 ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()
        event.accept()