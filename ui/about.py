# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import resource_rc

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(748, 329)
        AboutDialog.setModal(True)
        self.gridLayout = QGridLayout(AboutDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(AboutDialog)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(320, 280))
        self.label.setPixmap(QPixmap(u":/icon/images/h3D.jpg"))
        self.label.setScaledContents(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.aboutContent = QLabel(AboutDialog)
        self.aboutContent.setObjectName(u"aboutContent")
        self.aboutContent.setTextFormat(Qt.RichText)

        self.gridLayout.addWidget(self.aboutContent, 0, 1, 1, 3)

        self.pushButton = QPushButton(AboutDialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(100, 25))

        self.gridLayout.addWidget(self.pushButton, 1, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(273, 22, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 1, 1, 2)

        self.label_2 = QLabel(AboutDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)


        self.retranslateUi(AboutDialog)
        self.pushButton.clicked.connect(AboutDialog.close)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About", None))
        self.label.setText("")
        self.aboutContent.setText(QCoreApplication.translate("AboutDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/Images/logo_big.png\" width=\"150\" height=\"150\" /></p></td>\n"
"<td style=\" vertical-align:middle;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600;\">%(productName)s</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-"
                        "right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">%(Copyright)s</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Version %(version)s</span></p></td></tr></table></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("AboutDialog", u"OK", None))
        self.label_2.setText("")
    # retranslateUi

