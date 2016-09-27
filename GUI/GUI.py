# -*- coding: utf-8 -*-

"""
Module implementing HelloWindow.
"""
import sys, re, os, chardet
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog 

from Ui_GUI import Ui_Dialog


class HelloWindow(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
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
        sum=0
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if re.search('.txt$', file):
                    s=file+':\t'
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
                        if re.match(r'\n', word) and token==1:
                            phrase-=1
                            token=0
                    
                    sum+=subsum
                    s+=str(subsum)+'\t'+str(phrase//2)

                    self.textBrowser.append(s)
                    s=''
        self.label.setText('Total: '+str(sum)+' Chinese sentences\t'+str(phrase//2)+' phrases')
        
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    dlg=HelloWindow()
    dlg.show()
    sys.exit(app.exec())
