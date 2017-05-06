# -*- coding: utf-8 -*-

"""
Module implementing HelloWindow.
"""
import sys, re, os, csv, codecs
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
    count=0
    total_count=0
    expression=""
    num=0
    settle_exist_flag=0
    settle_click_flag=0
    total_flag=0
    thread_flag=0
    dict={}
    times=0

    def closeEvent(self, event):
        if not self.settle_exist_flag:
            return
        reply = QMessageBox.question(self, 'Message', 'Do you want to store them?',QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply==QMessageBox.Yes:
            name = QFileDialog.getSaveFileName(self,  'Save a file', 'C:\\Users\\hp\\Desktop', 'CSV(*.csv)')[0]
            if name:
                with open(name,"w",newline="") as datacsv:
                    writer = csv.writer(datacsv,dialect = ("excel"))
                    writer.writerow(["","File Name","Quantity"])
                    dict=self.dict
                    for dir in dict:
                        print(dir)
                        writer.writerow([dir])
                        total_count=0
                        for file in dict[dir]:
                            print(file)
                            if file=="Total":
                                total_count=dict[dir][file][0]
                            else:
                                writer.writerow(["",file,dict[dir][file][0]])
                        writer.writerow(["Total","", total_count])
                        print(dict)

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
        if self.thread_flag:
            QMessageBox.information(self,"Hold",  self.tr("Wait!"))
            return
        self.settle_click_flag=0
        self.count=0
        self.textBrowser.clear()
        self.textBrowser_3.clear()
        self.thread.terminate()
    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.expression=r"\n"
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.expression=r"。|！|？"
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        self.horizontalLayout_5.removeWidget(self.label_2)
        self.label_2.deleteLater()
        self.horizontalLayout_5.removeWidget(self.pushButton)
        self.pushButton.deleteLater()
        self.horizontalLayout_5.removeWidget(self.pushButton_2)
        self.pushButton_2.deleteLater()
        self.horizontalLayout_5.removeWidget(self.pushButton_3)
        self.pushButton_3.deleteLater()
        
        self.label_1 = QtWidgets.QLabel()
        self.label_1.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label_1)
        self.label_1.setText("Please input an expression")
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_5.addWidget(self.lineEdit)
        self.expression=""
        
    @pyqtSlot()
    def on_probtn_clicked(self):
        if not self.expression:
            if not self.pushButton:
                if not self.lineEdit.text():
                    QMessageBox.warning(self,"Warning!",  self.tr("Please input a pattern"))
                    return
                else:
                    self.expression=self.lineEdit.text()
                    return
            QMessageBox.warning(self,"Warning!",  self.tr("Please select a pattern"))
            return
        self.dict[self.directory]={}
        if self.thread_flag:
            QMessageBox.information(self,"Hold",  self.tr("Wait!"))
            return
        if self.directory:
            if not self.settle_exist_flag:
                self.settlebtn = QtWidgets.QPushButton()
                self.settlebtn.setObjectName("settlebtn")
                self.verticalLayout.addWidget(self.settlebtn)
                self.settlebtn.setText("Settle")
                self.settlebtn.clicked.connect(self.on_settlebtn_clicked)
                self.settle_exist_flag=1
                
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

            self.thread=Thread(self.directory, self.expression)
            self.thread.signal.connect(self.showresult)
            self.thread.start()
            self.thread_flag=1
        else:
            QMessageBox.information(self,"Information",  self.tr("Please select a directory first!"))  

    def showresult(self, subcount, file, amount, failure):
        if failure !='':
            if self.times==0:
                self.textBrowser_4 = QtWidgets.QTextBrowser()
                self.textBrowser_4.setEnabled(True)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(1)
                sizePolicy.setVerticalStretch(2)
                sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
                self.textBrowser_4.setSizePolicy(sizePolicy)
                self.textBrowser_4.setMinimumSize(QtCore.QSize(0, 80))
                self.textBrowser_4.setMaximumSize(QtCore.QSize(1000, 1000))
                self.textBrowser_4.setObjectName("textBrowser")
                self.verticalLayout.addWidget(self.textBrowser_4)
                self.times=1
            self.textBrowser_4.append(failure)
            failure ='' 
        if file=="xxx":
            self.label.setText('amount: '+amount)
        else:
            self.dict[self.directory][file]=[subcount]
            self.count+=subcount
            self.total_count+=subcount
            self.textBrowser.append(file)
            self.textBrowser_3.append(str(subcount))
            self.label.setText('Part'+str(self.num)+': '+str(self.count)+"  Expression: "+self.expression+"\t"+amount)
            self.label_total.setText("<html><body><p><span style='color:red'>Total:   "+str(self.total_count)+"</span></p></body></html>")
            am=re.split('/', amount)
            if am[0]==am[1]:
                self.thread_flag=0
                QMessageBox.information(self,"Information",  self.tr("Tasks finished!"))
                self.dict[self.directory]["Total"]=[self.total_count]

                
                

class Thread(QThread):
    
    signal=pyqtSignal(int, str, str, str)    
    
    def __init__(self, directory, expression):
        self.directory=directory
        self.expression=expression
        super(Thread, self).__init__()
    def run(self):
        file_array=[]
        amount=0
        failure=''
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                    if re.search('.txt$', file):
                        amount+=1
                        file_array.append(os.path.join(root, file))
                        self.signal.emit(0, 'xxx', str(amount), failure)
        current_amount=0
        if file_array:
            for file in file_array:
                file_name=re.sub(self.directory, '', file)
                #path=os.path.join(root, file)
                #print(path)
                try:
                    file=codecs.open(file, 'r', 'utf-8')
                except:
                    failure="failure occurs on: "+file_name
                try:
                    string=file.read()
                    file.close()
                except:
                    failure="codec error on: "+file_name
                pattern=re.compile(self.expression)
                sentences=re.split(pattern, string)
                count=len(sentences)-1
                
                current_amount+=1
                result_amount=str(current_amount)+'/'+str(amount)
                
                self.signal.emit(count, file_name, result_amount, failure)
        else:
             self.signal.emit(0, "no txt file", "0/0", "no txt file")
#            subsum, phrase, token, line=0, 0, 0, 0
#            for word in string:
#                if re.match(r'[\u3002\uff01\uff1f\uff1b]', word):
#                    subsum+=1
#                    token=1
#                elif re.match(r'\n', word):
#                    line+=1
#                    if token==0:
#                        phrase+=1
#                    token=0
#                    
#            phrase=phrase-line/2
#            current_amount+=1
#            result_amount=str(current_amount)+'/'+str(amount)
#            self.signal.emit(subsum, phrase, file_name, result_amount, failure)



if __name__=='__main__':
    app = QApplication(sys.argv)
    dlg=HelloWindow()
    dlg.show()
    sys.exit(app.exec())
