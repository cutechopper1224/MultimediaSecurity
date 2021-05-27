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
import math
from .mydialog import myDialog
from .Tree import *
from .Parameter import *
import time
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from random import SystemRandom
from sklearn.datasets import make_spd_matrix


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
        self.start = FILE_START
        self.end = FILE_END
        self.keyword = []
        self.m = 1500
        self.m_p = 100
        self.initialize()

    def initialize(self):
        f = open(f"keyword.txt", "r")
        first = f.read()
        f.close()
        keywords = first.split('\n')
        self.keyword = keywords[:-1]

    def inGuiEvent(self):
        self.setWindowTitle('Ptt文章搜尋器- Data Owner')
        self.btnEncrypt.clicked.connect(self.showPassForm)
        self.btnTree.clicked.connect(self.generateTreeIndex)
        self.btnSec1.clicked.connect(self.generateBDMRSIndex)
        self.btnSec2.clicked.connect(self.generateEDMRSIndex)
        self.btnProduct.clicked.connect(self.generateIndex)

    
    def generateIndex(self):
        database = {}

        print("建立資料庫索引中...")


        for i in range(self.num):
            print(f'Indexing file {i}')
            f = open(f"rawText/{i}.json", "r")
            context = f.read()
            try:
                j = json.loads(context)
            except:
                continue

            title = []
            content = []
            push = []

            count = 0

           
            j_content = j['content'].split('※ 發信站: 批踢踢實業坊')[0]

            try:
                j_title = j_content.split('\n')[1]
                j_content = j_content.split(j_title)[1]
                j_title = j_title.split('標題')[1].split('時間')[-2]
            except:
                j_title = ''

            try:
                j_push = j['content'].split('※ 發信站: 批踢踢實業坊')[1]
            except:
                j_push = ''

            title = [j_title.count(keyword) for keyword in self.keyword]
            content = [j_content.count(keyword) for keyword in self.keyword]
            push = [j_push.count(keyword) for keyword in self.keyword]

            term = title + content + push

            inverted = [(x, term[x])  for x in range(len(term)) if term[x] != 0]
            database[i] = inverted


        f = open(f"index.json", "w")
        f.write(json.dumps(database))
        f.close()



    def createBasicSecret(self, filename='basic_secret'):
        print('Generating Basic serect ...')

        cryptogen = SystemRandom()
        sec = [cryptogen.randrange(2) for i in range(self.m + self.m_p)]
        index1 = cryptogen.randrange(10 ** 6)
        index2 = cryptogen.randrange(10 ** 6)



        cipher = ''
        for s in sec:
            cipher += str(s)
        cipher += '\n'
        cipher += str(index1)
        cipher += '\n'
        cipher += str(index2)



        outputFile = filename + '.bin'

        with open(outputFile, "wb") as f:
            f.write(cipher.encode())


        #print(np.linalg.inv(M1))
        #print(M1.shape)




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


    def generateTreeIndex(self):
        currentTime = time.time()
        if os.path.isfile('plaintree.json'):
            self.label1.setText('已經產生過樹狀索引')
            return


        if not os.path.isfile('tf.json'):
            self.generateTF()

        if not os.path.isfile('idf.json'):
            self.generateIDF()



        # Load TF table
        f = open(f"tf.json", "r")
        str1 = f.read()

        n = self.end - self.start + 1


        Freqs = np.array(json.loads(str1))
        print(Freqs.shape)


        # BuildIndexTree



        serial = 0
        CurrentNodeSet = []
        AllNodes = []

        for i in range(n):
            node = TreeNode(serial, i)
            node.D = Freqs[i]
            CurrentNodeSet.append(node)
            serial += 1

        print(CurrentNodeSet[-1].ID)
        print(CurrentNodeSet[-1].D)

        AllNodes = AllNodes + CurrentNodeSet

        count = 0
        while len(CurrentNodeSet) > 1:
            count = count + 1
            print(f'Tier {count}...')
            TempNodeSet = []
            if len(CurrentNodeSet) % 2 == 0:
                for p in range(0, len(CurrentNodeSet), 2):
                    u1 = CurrentNodeSet[p]
                    u2 = CurrentNodeSet[p+1]
                    u = TreeNode(serial, 0)
                    serial += 1
                    u.PL = u1.ID
                    u.PR = u2.ID
                    u.D = [max(u1.D[x], u2.D[x]) for x in range(self.m)]
                    TempNodeSet.append(u)

            elif len(CurrentNodeSet) != 3:
                h = (len(CurrentNodeSet) - 1) // 2
                for p in range(0, h + 1, 2):
                    u1 = CurrentNodeSet[p]
                    u2 = CurrentNodeSet[p+1]
                    u = TreeNode(serial, 0)
                    serial += 1
                    u.PL = u1.ID
                    u.PR = u2.ID
                    u.D = [max(u1.D[x], u2.D[x]) for x in range(self.m)]
                    TempNodeSet.append(u)

                u1 = CurrentNodeSet[2 * h - 2]
                u2 = CurrentNodeSet[2 * h - 1]
                u = TreeNode(serial, 0)
                serial += 1
                u.PL = u1.ID
                u.PR = u2.ID
                u.D = [max(u1.D[x], u2.D[x]) for x in range(self.m)]
                TempNodeSet.append(u)

                u1 = u
                u2 = CurrentNodeSet[2 * h]
                u = TreeNode(serial, 0)
                serial += 1
                u.PL = u1.ID
                u.PR = u2.ID
                u.D = [max(u1.D[x], u2.D[x]) for x in range(self.m)]
                TempNodeSet.append(u)

            else:
                u1 = CurrentNodeSet[0]
                u2 = CurrentNodeSet[1]
                u = TreeNode(serial, 0)
                serial += 1
                u.PL = u1.ID
                u.PR = u2.ID
                u.D = [max(u1.D[x], u2.D[x]) for x in range(self.m)]
                TempNodeSet.append(u)

                u1 = CurrentNodeSet[1]
                u2 = CurrentNodeSet[2]
                u = TreeNode(serial, 0)
                serial += 1
                u.PL = u1.ID
                u.PR = u2.ID
                u.D = [max(u1.D[x], u2.D[x]) for x in range(self.m)]
                TempNodeSet.append(u)


            AllNodes = AllNodes + TempNodeSet
            CurrentNodeSet = TempNodeSet

        used_time = time.time() - currentTime
        self.label2.setText(f'花費時間:{used_time}秒')

        print('Root ID:')
        print(CurrentNodeSet[0].ID)
        print('Nodes amount:')
        print(len(AllNodes))

        sorted(AllNodes, key=lambda x: x.ID)
        f = open(f"plaintree.json", "w")
        f.write(json.dumps(AllNodes, cls=TreeNodeEncoder))
        f.close()



    def generateBDMRSIndex(self):
        currentTime = time.time()

        if os.path.isfile('BDMRStree.json'):
            self.label1.setText('已經產生過該索引')
            return

        print("Generating BDMRS index...")
        if not os.path.isfile('basic_secret.bin'):
            self.createBasicSecret()

        if not os.path.isfile('plaintree.json'):
            self.generateTreeIndex()

        f = open('basic_secret.bin', "rb")
        cipherdata = f.read()
        f.close()
        cipherdata = cipherdata.decode()
        cipher = cipherdata.split('\n')
        S = cipher[0]
        index1 = int(cipher[1])
        index2 = int(cipher[2])

        M1 = make_spd_matrix(self.m, random_state = index1)
        M2 = make_spd_matrix(self.m, random_state = index2)
        cryptogen = SystemRandom()


        f = open(f"plaintree.json", "r")
        str1 = f.read()

        n = self.end - self.start + 1
        Nodes = []
        SecureNodes = []
        AllNodes = json.loads(str1)
        for Node in AllNodes:
            print(f"Processing Node {Node['ID']}")
            securenode = SecureTreeNode(Node['ID'], Node['FID'])
            securenode.PL = Node['PL']
            securenode.PR = Node['PR']
            Du = np.array(Node['D'])

            Du_1 = np.zeros(self.m)
            Du_2 = np.zeros(self.m)
            for i in range(self.m):
                if S[i] == '0':
                    Du_1[i] = Du[i]
                    Du_2[i] = Du[i]

                else:
                    Du_1[i] = cryptogen.random()
                    Du_2[i] = Du[i] - Du_1[i]

            Iu_1 = M1.dot(Du_1)
            Iu_2 = M2.dot(Du_2)
            Iu = list(Iu_1) + list(Iu_2)
            print(Iu_1)

            securenode.Iu = Iu

            SecureNodes.append(securenode)

        used_time = time.time() - currentTime
        self.label2.setText(f'花費時間:{used_time}秒')


        f = open(f"BDMRStree.json", "w")
        f.write(json.dumps(SecureNodes, cls=TreeNodeEncoder))
        f.close()


    def generateEDMRSIndex(self):
        currentTime = time.time()

        if os.path.isfile('EDMRStree.json'):
            self.label1.setText('已經產生過該索引')
            return

        print("Generating EDMRS index...")
        if not os.path.isfile('basic_secret_EDMRS.bin'):
            self.createBasicSecret('basic_secret_EDMRS')

        if not os.path.isfile('plaintree.json'):
            self.generateTreeIndex()

        f = open('basic_secret_EDMRS.bin', "rb")
        cipherdata = f.read()
        f.close()
        cipherdata = cipherdata.decode()
        cipher = cipherdata.split('\n')
        S = cipher[0]
        index1 = int(cipher[1])
        index2 = int(cipher[2])

        M1 = make_spd_matrix(self.m + self.m_p, random_state = index1)
        M2 = make_spd_matrix(self.m + self.m_p, random_state = index2)
        cryptogen = SystemRandom()


        f = open(f"plaintree.json", "r")
        str1 = f.read()

        n = self.end - self.start + 1
        Nodes = []
        SecureNodes = []
        AllNodes = json.loads(str1)
        for Node in AllNodes:
            print(f"Processing Node {Node['ID']}")
            securenode = SecureTreeNode(Node['ID'], Node['FID'])
            securenode.PL = Node['PL']
            securenode.PR = Node['PR']
            Du = np.array(Node['D'])
            phantom = np.random.rand(self.m_p)
            Du = np.append(Du, phantom)

            Du_1 = np.zeros(self.m + self.m_p)
            Du_2 = np.zeros(self.m + self.m_p)
            for i in range(self.m + self.m_p):
                if S[i] == '0':
                    Du_1[i] = Du[i]
                    Du_2[i] = Du[i]

                else:
                    Du_1[i] = cryptogen.random()
                    Du_2[i] = Du[i] - Du_1[i]

            Iu_1 = M1.dot(Du_1)
            Iu_2 = M2.dot(Du_2)
            Iu = list(Iu_1) + list(Iu_2)
            print(Iu_1)

            securenode.Iu = Iu

            SecureNodes.append(securenode)

        used_time = time.time() - currentTime
        self.label2.setText(f'花費時間:{used_time}秒')


        f = open(f"EDMRStree.json", "w")
        f.write(json.dumps(SecureNodes, cls=TreeNodeEncoder))
        f.close()






    def generateIDF(self):
        print("Calculating IDF")



        N = self.end - self.start + 1
        database = np.zeros(self.m)

        max_term = 0
        for k in range(self.start, self.end + 1):

            print(f"Calculating IDF for {k}")
            f = open(f"rawText/{k}.json", "r")
            context = f.read()
            try:
                j = json.loads(context)
            except:
                pass

            j_content = j['content'].split('※ 發信站: 批踢踢實業坊')[0]

            try:
                j_title = j_content.split('\n')[1]
                j_content = j_content.split(j_title)[1]
                j_title = j_title.split('標題')[1].split('時間')[-2]
            except:
                j_title = ''

            try:
                j_push = j['content'].split('※ 發信站: 批踢踢實業坊')[1]
            except:
                j_push = ''

            title = [j_title.count(keyword) for keyword in self.keyword]
            content = [j_content.count(keyword) for keyword in self.keyword]
            push = [j_push.count(keyword) for keyword in self.keyword]

            term = title + content + push



            for i in range(len(term)):
                if term[i] != 0:
                    database[i] += 1


        IDF_p = [np.log(1 + N / database[i]) if database[i] > 0 else 0 for i in range(self.m)]
        #q = math.sqrt(np.sum(np.power(IDF_p, 2)))

        #IDF = list(np.array(IDF_p) / q)

        f = open(f"idf.json", "w")
        f.write(json.dumps(IDF_p))
        f.close()


    def generateTF(self):
        database = {}
        Freqs = []
        eps = 0.5
        for k in range(self.start, self.end + 1):
            print(f"Calculating TF for {k}")


            f = open(f"rawText/{k}.json", "r")

            context = f.read()
            try:
                j = json.loads(context)
            except:
                pass

            frequency = {}

            j_content = j['content'].split('※ 發信站: 批踢踢實業坊')[0]

            try:
                j_title = j_content.split('\n')[1]
                j_content = j_content.split(j_title)[1]
                j_title = j_title.split('標題')[1].split('時間')[-2]
            except:
                j_title = ''

            try:
                j_push = j['content'].split('※ 發信站: 批踢踢實業坊')[1]
            except:
                j_push = ''

            f_title = [1 + np.log(j_title.count(keyword) + eps) for keyword in self.keyword]
            f_content = [1 + np.log(j_content.count(keyword) + eps) for keyword in self.keyword]
            f_push = [1 + np.log(j_push.count(keyword) + eps) for keyword in self.keyword]

            f3 = f_title + f_content + f_push
            f3 = np.array(f3)

            q = math.sqrt(np.sum(np.power(f3, 2)))


            frequency = f3 / q

            Freqs.append(list(frequency))


        f = open(f"tf.json", "w")
        f.write(json.dumps(Freqs))
        f.close()



