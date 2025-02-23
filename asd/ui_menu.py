# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menu.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(762, 558)
        self.menu_label = QLabel(Form)
        self.menu_label.setObjectName(u"menu_label")
        self.menu_label.setGeometry(QRect(260, 120, 141, 31))
        self.form_button = QPushButton(Form)
        self.form_button.setObjectName(u"form_button")
        self.form_button.setGeometry(QRect(260, 200, 181, 41))
        self.db_view_button = QPushButton(Form)
        self.db_view_button.setObjectName(u"db_view_button")
        self.db_view_button.setGeometry(QRect(260, 260, 181, 41))
        self.log_out_button = QPushButton(Form)
        self.log_out_button.setObjectName(u"log_out_button")
        self.log_out_button.setGeometry(QRect(260, 330, 181, 41))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.menu_label.setText(QCoreApplication.translate("Form", u"Menu Screen", None))
        self.form_button.setText(QCoreApplication.translate("Form", u"Add a new patient", None))
        self.db_view_button.setText(QCoreApplication.translate("Form", u"View all patients", None))
        self.log_out_button.setText(QCoreApplication.translate("Form", u"Log Out", None))
    # retranslateUi

