# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        Form.setStyleSheet(u"QMainWindow {\n"
"    background-color: #F7F8FA;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #4A90E2;\n"
"    color: white;\n"
"    border: 1px solid #4A90E2;\n"
"    border-radius: 5px;\n"
"    font-size: 14px;\n"
"    padding: 8px 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #50C8C6;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: white;\n"
"    border: 1px solid #B3E5FC;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #4A4A4A;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QMessageBox {\n"
"    background-color: #FAFAFA;\n"
"    color: #4A4A4A;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QMessageBox[success=true] {\n"
"    background-color: #2ECC71;\n"
"    color: white;\n"
"}\n"
"\n"
"QMessageBox[error=true] {\n"
"    background-color: #E57373;\n"
"    color: white;\n"
"}\n"
"")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

