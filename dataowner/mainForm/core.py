# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:30:15 2021

@author: user
"""

from PyQt5 import QtWidgets, uic, QtGui
import os

import glob
import random
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests
from bs4 import BeautifulSoup as soup
import json
import numpy as np
from .mydialog import myDialog
import time
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

path = os.getcwd()
qtCreatorFile = path + os.sep + "DataOwner.ui"
iconFile = path + os.sep + "logo.png"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

salt = b'\xd0\x18\xa7QM\xd6\x9b\xebxu\xe4\xed\xa8\x83\xf6\xa3/\x01\x9c\x9e\x86n\xda;\x10EdD\xf7\x932\xcc'


class Article():
    def __init__(self):
        self.title = ""
        self.content = ""
        self.push = ""

class MainUi(QtWidgets.QMainWindow, Ui_MainWindow): 
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(iconFile))
        self.inGuiEvent()
        self.num = 105961
        self.dialog = None
  

    def inGuiEvent(self):
        self.setWindowTitle('Ptt文章搜尋器- Data Owner')
        self.btnEncrypt.clicked.connect(self.showPassForm)
        

    def showPassForm(self):
        self.dialog = myDialog()
        self.dialog.resize(713, 300)
        self.dialog.setWindowIcon(QtGui.QIcon(iconFile))
               
        self.dialog.edit = QLineEdit(self.dialog)
        self.dialog.edit.resize(531,41)
        self.dialog.edit.move(80,100)
        self.dialog.edit.setEchoMode(QLineEdit.Password)
        self.dialog.edit.setFont(QFont("Agency FB",24,QFont.Bold))
        
        
        
        btn= QPushButton('確定',self.dialog)
        btn.move(260,220)
        btn.resize(160,61)
        btn.clicked.connect(self.EncryptData)
        
        self.dialog.setWindowTitle("請輸入密碼")
       
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()


    def EncryptData(self):
        print('Encrypting Database...')
        #print(self.dialog.edit.text())
        password = self.dialog.edit.text()
        self.dialog.close()
        self.label1.setText('正在對原始資料進行加密...')
        currentTime = time.time()

        for i in range(self.num):
            try:
                print(f'Encrypting file {i} ...')
                f = open(f"rawText/{i}.json", "r")
                context = f.read()
                f.close()
                j = json.loads(context)
            
                #Generate Key
                
                key = PBKDF2(password, salt, dkLen=32)
            
                #Encrypt Data

                data = j['content'].encode()
                cipher = AES.new(key, AES.MODE_CFB)
                cipheredData = cipher.encrypt(data)
                    
                outputFile = f"Encrypted/{i}.bin"

                with open(outputFile, "wb") as f:
                    f.write(cipher.iv)
                    f.write(cipheredData)
            except:
                pass

        '''
        #Decrypt Data
        inputFile = f"Encrypted/100.bin"
        with open(inputFile, "rb") as f:
            iv = f.read(16)
            cipheredData = f.read()

        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        originalData = cipher.decrypt(cipheredData)
        print(originalData.decode())
        '''

        used_time = time.time() - currentTime
        self.label2.setText(f'花費時間:{used_time}秒')


        
