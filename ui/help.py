# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'help.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtWebEngineWidgets import QWebEngineView



class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName(u"HelpDialog")
        HelpDialog.resize(581, 390)
        HelpDialog.setModal(True)
        self.gridLayout = QGridLayout(HelpDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(HelpDialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(100, 25))

        self.horizontalLayout.addWidget(self.pushButton)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.webView = QWebEngineView(HelpDialog)
        self.webView.setObjectName(u"webView")
        self.webView.setUrl(QUrl(u"about:blank"))

        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)


        self.retranslateUi(HelpDialog)
        self.pushButton.clicked.connect(HelpDialog.close)

        QMetaObject.connectSlotsByName(HelpDialog)
    # setupUi

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(QCoreApplication.translate("HelpDialog", u"Help", None))
        self.pushButton.setText(QCoreApplication.translate("HelpDialog", u"OK", None))
    # retranslateUi

