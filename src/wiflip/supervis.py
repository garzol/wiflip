# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/garzol/git/wiflip_tracer/ui/supervis.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SupervisDialog(object):
    def setupUi(self, SupervisDialog):
        SupervisDialog.setObjectName("SupervisDialog")
        SupervisDialog.resize(608, 659)
        SupervisDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(SupervisDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(SupervisDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.superButton = QtWidgets.QPushButton(self.groupBox)
        self.superButton.setObjectName("superButton")
        self.gridLayout.addWidget(self.superButton, 0, 0, 1, 1)
        self.leaveButton = QtWidgets.QPushButton(self.groupBox)
        self.leaveButton.setMinimumSize(QtCore.QSize(0, 40))
        self.leaveButton.setObjectName("leaveButton")
        self.gridLayout.addWidget(self.leaveButton, 1, 0, 1, 1)
        self.panicButton = QtWidgets.QPushButton(self.groupBox)
        self.panicButton.setMinimumSize(QtCore.QSize(0, 40))
        self.panicButton.setObjectName("panicButton")
        self.gridLayout.addWidget(self.panicButton, 2, 0, 1, 1)
        self.labelStatus = QtWidgets.QLabel(self.groupBox)
        self.labelStatus.setMaximumSize(QtCore.QSize(32, 32))
        self.labelStatus.setText("")
        self.labelStatus.setPixmap(QtGui.QPixmap(":/x/ledgrey.png"))
        self.labelStatus.setScaledContents(True)
        self.labelStatus.setObjectName("labelStatus")
        self.gridLayout.addWidget(self.labelStatus, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.scrollArea = QtWidgets.QScrollArea(SupervisDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 582, 431))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.buttonBox = QtWidgets.QDialogButtonBox(SupervisDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SupervisDialog)
        self.buttonBox.accepted.connect(SupervisDialog.accept)
        self.buttonBox.rejected.connect(SupervisDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SupervisDialog)

    def retranslateUi(self, SupervisDialog):
        _translate = QtCore.QCoreApplication.translate
        SupervisDialog.setWindowTitle(_translate("SupervisDialog", "Supervisor"))
        self.groupBox.setTitle(_translate("SupervisDialog", "Control"))
        self.superButton.setText(_translate("SupervisDialog", "Super"))
        self.leaveButton.setText(_translate("SupervisDialog", "Leave control"))
        self.panicButton.setText(_translate("SupervisDialog", "Panic/Reset pinball"))
#import wiflip.resource_rc
