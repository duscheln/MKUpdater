# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(290, 451)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(290, 450))
        Dialog.setMaximumSize(QtCore.QSize(300, 451))
        Dialog.setSizeGripEnabled(False)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.userNametxt = QtWidgets.QLineEdit(Dialog)
        self.userNametxt.setPlaceholderText("")
        self.userNametxt.setObjectName("userNametxt")
        self.verticalLayout.addWidget(self.userNametxt)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.passwordtxt = QtWidgets.QLineEdit(Dialog)
        self.passwordtxt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordtxt.setPlaceholderText("")
        self.passwordtxt.setObjectName("passwordtxt")
        self.verticalLayout.addWidget(self.passwordtxt)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.unitClubBtn = QtWidgets.QPushButton(Dialog)
        self.unitClubBtn.setObjectName("unitClubBtn")
        self.verticalLayout_2.addWidget(self.unitClubBtn)
        self.inTouchBtn = QtWidgets.QPushButton(Dialog)
        self.inTouchBtn.setObjectName("inTouchBtn")
        self.verticalLayout_2.addWidget(self.inTouchBtn)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setCenterOnScroll(True)
        self.plainTextEdit.setPlaceholderText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_3.addWidget(self.plainTextEdit)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.inTouchBtn.raise_()
        self.userNametxt.raise_()
        self.passwordtxt.raise_()
        self.unitClubBtn.raise_()
        self.plainTextEdit.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.line.raise_()
        self.unitClubBtn.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MK Updater"))
        self.label.setText(_translate("Dialog", "Username"))
        self.label_2.setText(_translate("Dialog", "Password"))
        self.unitClubBtn.setText(_translate("Dialog", "Unit Club"))
        self.inTouchBtn.setText(_translate("Dialog", "MK InTouch"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

