# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setGeometry(QRect(0, 0, 801, 611))
        self.name_label = QLabel(self.centralwidget)
        self.name_label.setObjectName(u"name_label")
        self.name_label.setGeometry(QRect(120, 110, 49, 16))
        self.name_input = QLineEdit(self.centralwidget)
        self.name_input.setObjectName(u"name_input")
        self.name_input.setGeometry(QRect(120, 140, 161, 24))
        self.age_label = QLabel(self.centralwidget)
        self.age_label.setObjectName(u"age_label")
        self.age_label.setGeometry(QRect(120, 190, 49, 16))
        self.textEdit_2 = QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(470, 140, 241, 91))
        self.male_radio = QRadioButton(self.centralwidget)
        self.male_radio.setObjectName(u"male_radio")
        self.male_radio.setGeometry(QRect(180, 240, 91, 22))
        self.female_radio = QRadioButton(self.centralwidget)
        self.female_radio.setObjectName(u"female_radio")
        self.female_radio.setGeometry(QRect(180, 270, 91, 22))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(470, 260, 91, 16))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(470, 110, 81, 16))
        self.submit_button = QPushButton(self.centralwidget)
        self.submit_button.setObjectName(u"submit_button")
        self.submit_button.setGeometry(QRect(420, 380, 131, 51))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(180, 40, 381, 41))
        self.label_2.setStyleSheet(u"font: 700 20pt \"Segoe UI\";")
        self.doubleSpinBox = QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setGeometry(QRect(180, 190, 62, 25))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(120, 240, 49, 16))
        self.back_button = QPushButton(self.centralwidget)
        self.back_button.setObjectName(u"back_button")
        self.back_button.setGeometry(QRect(220, 380, 131, 51))
        self.doubleSpinBox_3 = QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_3.setObjectName(u"doubleSpinBox_3")
        self.doubleSpinBox_3.setGeometry(QRect(570, 260, 62, 25))

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.name_label.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.name_input.setText("")
        self.age_label.setText(QCoreApplication.translate("MainWindow", u"Age", None))
        self.male_radio.setText(QCoreApplication.translate("MainWindow", u"Male", None))
        self.female_radio.setText(QCoreApplication.translate("MainWindow", u"Female", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"CARS score", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Observations", None))
        self.submit_button.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Input patient Information", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Gender", None))
        self.back_button.setText(QCoreApplication.translate("MainWindow", u"Back", None))
    # retranslateUi

