# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Python\GUI\GUI.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(390, 290)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        Dialog.setSizeGripEnabled(True)
        self.selectbtn = QtWidgets.QPushButton(Dialog)
        self.selectbtn.setGeometry(QtCore.QRect(20, 20, 101, 31))
        self.selectbtn.setObjectName("selectbtn")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(130, 20, 171, 31))
        self.textEdit.setObjectName("textEdit")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 60, 361, 181))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 245, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.probtn = QtWidgets.QPushButton(Dialog)
        self.probtn.setGeometry(QtCore.QRect(310, 20, 75, 31))
        self.probtn.setObjectName("probtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CountSent"))
        self.selectbtn.setText(_translate("Dialog", "SelectDirectory"))
        self.label.setText(_translate("Dialog", "Total："))
        self.probtn.setText(_translate("Dialog", "Process"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

