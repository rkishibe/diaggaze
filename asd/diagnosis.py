import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout,  QTableWidgetItem, QLabel, QMessageBox, QDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

image_directory = "../../dataset/Images/TCImages"

class ImagePopup(QDialog):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(400, 200, 600, 400)

        layout = QVBoxLayout()

        # Load and display the image
        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            QMessageBox.critical(self, "Error", f"Failed to load image: {image_path}")
            self.close()
        else:
            self.image_label.setPixmap(pixmap.scaled(580, 380, aspectRatioMode=1))  # Resize image
            layout.addWidget(self.image_label)

        self.setLayout(layout)


class DiagnosisScreen(QWidget):
    def __init__(self, stacked_widget, model):
        super().__init__()
        self.stacked_widget = stacked_widget
        loadUi('diagnosis.ui',self)

        self.diagnosis_label.setAlignment(Qt.AlignCenter)
        self.diagnosis_label.setStyleSheet("font-size: 20px; font-weight: bold;")


        # Main layout
        layout = QVBoxLayout(self)

        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Table to display image names
        self.table_widget.setColumnCount(1)
        self.table_widget.setHorizontalHeaderLabels(["Image Name"])
        self.table_widget.cellDoubleClicked.connect(self.open_image_popup)
        #layout.addWidget(self.table_widget)

        self.image_label = ImageDropLabel(model)
        
        layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.load_images()

    def load_images(self):
        """Loads image names from the directory into the table."""
        if not os.path.exists(image_directory):
            QMessageBox.critical(self, "Error", f"Directory not found: {image_directory}")
            return

        # Get list of image files
        image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        self.table_widget.setRowCount(len(image_files))

        for row, image_name in enumerate(image_files):
            self.table_widget.setItem(row, 0, QTableWidgetItem(image_name))

    def open_image_popup(self, row, column):
        """Opens a popup to display the selected image."""
        image_name = self.table_widget.item(row, column).text()
        image_path = os.path.join(image_directory, image_name)

        # Show image in a popup
        self.image_popup = ImagePopup(image_path)
        self.image_popup.exec_()

class ImageDropLabel(QLabel):
    def __init__(self, model):
        super().__init__()
        self.setText("Drag and Drop an Image Here")
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(100, 100)
        self.move(200,200)
        self.setStyleSheet("border: 2px dashed #aaa; font-size: 16px; padding: 20px;")
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
            self.setText(f"Prediction: {result}")  # Display result

    def predict_image(self, file_path):
        """ Convert image to tensor & run prediction """
        img = QImage(file_path)
        #img = img.scaled(128, 128, Qt.KeepAspectRatio)  # Resize to match model input
        # buffer = img.bits().asstring(img.width() * img.height() * 4)  # Convert to bytes
        # arr = np.frombuffer(buffer, dtype=np.uint8).reshape(img.height(), img.width(), 4)  # Convert to NumPy array

        # # Preprocess: Convert to grayscale/RGB, normalize, reshape for the model
        # arr = arr[..., :3] / 255.0  # Remove alpha channel, normalize
        # arr = np.expand_dims(arr, axis=0)  # Add batch dimension

        # # Predict using ML model
        # prediction = self.model.predict(arr)
        # return np.argmax(prediction)  # Return predicted class index
