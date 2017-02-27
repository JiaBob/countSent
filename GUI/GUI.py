# -*- coding: utf-8 -*-

"""
Module implementing HelloWindow.
"""
import sys, re, os, chardet
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog 

from Ui_GUI import Ui_Dialog


class HelloWindow(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    sum=0
    phsum=0
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
    def on_probtn_clicked(self):

        self.thread=Thread(self.directory)
        self.thread.signal.connect(self.showresult)
        self.thread.start()


    def showresult(self, subsum, phrase, file, amount):
        self.sum+=subsum
        self.phsum+=phrase
        self.textBrowser.append(file)
        self.textBrowser_2.append(str(subsum))
        self.textBrowser_3.append(str(phrase))
        self.label.setText('Total:  '+str(self.sum)+' sentences   '+str(self.phsum//2)+' phrases   '+amount)

class Thread(QThread):
    
    signal=pyqtSignal(int, int, str, str)    
    
    def __init__(self, directory):
        self.directory=directory
        super(Thread, self).__init__()
        print(self.directory)
    def run(self):
        sum=phsum=0
        print("asd")
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
