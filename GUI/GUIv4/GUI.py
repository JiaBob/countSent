# -*- coding: utf-8 -*-

"""
Module implementing HelloWindow.
"""
import sys, re, os, chardet
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import *

from Ui_GUI import Ui_Dialog


class HelloWindow(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    total_s=0
    total_ph=0
    num=0
    sum=0
    phsum=0
    settle_exist_flag=1
    settle_click_flag=0
    total_flag=0
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(HelloWindow, self).__init__(parent)
        self.setupUi(self)
        self.directory=''
    @pyqtSlot()
    def on_selectbtn_clicked(self):
        directoryUri = QFileDialog.getExistingDirectory(self,  'Select a Directory', 'C:\\Users\\hp\\Desktop')
        self.directory=directoryUri
        self.textEdit.setText(directoryUri)
    @pyqtSlot()
    def on_settlebtn_clicked(self):
        self.settle_click_flag=0
        self.sum=0
        self.phsum=0
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        self.thread.terminate()
        
    @pyqtSlot()
    def on_probtn_clicked(self):
        if self.directory:
                
            if self.settle_exist_flag:
                self.settlebtn = QtWidgets.QPushButton()
                self.settlebtn.setObjectName("settlebtn")
                self.verticalLayout.addWidget(self.settlebtn)
                self.settlebtn.setText("Settle")
                self.settlebtn.clicked.connect(self.on_settlebtn_clicked)
                self.settle_exist_flag=0
                
            if not self.total_flag:
                self.total_flag=1
                self.label_total = QtWidgets.QLabel()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(1)
                sizePolicy.setVerticalStretch(1)
                sizePolicy.setHeightForWidth(self.label_total.sizePolicy().hasHeightForWidth())
                self.label_total.setSizePolicy(sizePolicy)
                self.label_total.setMaximumSize(QtCore.QSize(16777215, 30))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                font.setBold(False)
                font.setWeight(50)
                self.label_total.setFont(font)
                self.label_total.setObjectName("label_total")
                self.verticalLayout.addWidget(self.label_total)
                
            if not self.settle_click_flag:
                self.num+=1 # num + 1, when there is no new-created label 
                self.settle_click_flag=1
                self.label = QtWidgets.QLabel()
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(1)
                sizePolicy.setVerticalStretch(1)
                sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
                self.label.setSizePolicy(sizePolicy)
                self.label.setMaximumSize(QtCore.QSize(16777215, 30))
                font = QtGui.QFont()
                font.setFamily("Times New Roman")
                font.setPointSize(14)
                font.setBold(False)
                font.setWeight(50)
                self.label.setFont(font)
                self.label.setObjectName("label")
                self.verticalLayout.addWidget(self.label)

            self.thread=Thread(self.directory)
            self.thread.signal.connect(self.showresult)
            self.thread.start()
        else:
            QMessageBox.information(self,"Information",  self.tr("Please select a directory first!"))  

    def showresult(self, subsum, phrase, file, amount):
        self.sum+=subsum
        self.total_s+=subsum
        self.phsum+=phrase
        self.total_ph+=phrase
        self.textBrowser.append(file)
        self.textBrowser_2.append(str(subsum))
        self.textBrowser_3.append(str(phrase))
        self.label.setText('Part'+str(self.num)+':  '+str(self.sum)+' sentences   '+str(self.phsum//2)+' phrases   '+amount)
        self.label_total.setText("<html><body><p><span style='color:red'>Total:   "+str(self.total_s)+" sentences   "+str(self.total_ph//2)+" phrases   </span></p></body></html>")

class Thread(QThread):
    
    signal=pyqtSignal(int, int, str, str)    
    
    def __init__(self, directory):
        self.directory=directory
        super(Thread, self).__init__()
        print(self.directory)
    def run(self):
        sum=phsum=0
        for root, dirs, files in os.walk(self.directory):
            amount=0
            current_amount=0
            file_array=[]
            for file in files:
                if re.search('.txt$', file):
                    amount+=1
                    file_array.append(file)
            for file in file_array:
                file_name=file
                path=os.path.join(root, file)
                file=open(path, 'rb+')
                string=file.read()
                coding=chardet.detect(string)['encoding']
                if coding:
                    string=string.decode(coding)
                else:
                    string=''
                subsum=0
                phrase=0
                token=0
                for word in string:
                    if re.match(r'[\u3002\uff01\uff1f]', word):
                        subsum+=1
                        token=1
                    elif re.match(r'\n', word):
                        phrase+=1
                        if token==1:
                            phrase-=1
                            token=0
                            
                current_amount+=1
                phsum+=phrase
                sum+=subsum
                result_amount=str(current_amount)+'/'+str(amount)
                self.signal.emit(subsum, phrase, file_name, result_amount)
                print(subsum)



if __name__=='__main__':
    app = QApplication(sys.argv)
    dlg=HelloWindow()
    dlg.show()
    sys.exit(app.exec())
