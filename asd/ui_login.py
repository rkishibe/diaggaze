# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(760, 499)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet(u"")
        self.title_label = QLabel(Form)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(250, 100, 231, 61))
        self.title_label.setStyleSheet(u"font-size: 20px; font-weight: bold;")
        self.username_label = QLabel(Form)
        self.username_label.setObjectName(u"username_label")
        self.username_label.setGeometry(QRect(260, 170, 81, 16))
        self.username_input = QLineEdit(Form)
        self.username_input.setObjectName(u"username_input")
        self.username_input.setGeometry(QRect(260, 200, 181, 31))
        self.username_input.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.password_label = QLabel(Form)
        self.password_label.setObjectName(u"password_label")
        self.password_label.setGeometry(QRect(260, 250, 81, 21))
        self.password_input = QLineEdit(Form)
        self.password_input.setObjectName(u"password_input")
        self.password_input.setGeometry(QRect(260, 280, 181, 31))
        self.login_button = QPushButton(Form)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setGeometry(QRect(290, 340, 111, 41))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.title_label.setText(QCoreApplication.translate("Form", u"Welcome to the app!", None))
        self.username_label.setText(QCoreApplication.translate("Form", u"Username", None))
        self.password_label.setText(QCoreApplication.translate("Form", u"Password", None))
        self.login_button.setText(QCoreApplication.translate("Form", u"Login", None))
    # retranslateUi

