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
import time
from dataowner.mainForm.mydialog import myDialog
from base64 import b64encode, b64decode
path = os.getcwd()
qtCreatorFile = path + os.sep + "SSE.ui"
iconFile = path + os.sep + "logo.png"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from random import SystemRandom
from dataowner.mainForm.Tree import TreeNode, SecureTreeNode
from sklearn.datasets import make_spd_matrix
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
        self.dialog = None
        self.num = 105961
        self.start = 99001
        self.end = 100000
        self.m = 1500
        self.m_p = 100
        self.database = np.zeros((self.num, 1500))
        self.keyword = []
        self.maxSearchTerm = 5
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000)
        self.spinBox.setValue(100)

        self.searchResult = []
        self.searchMode = 0
        self.createDatabase()
        self.randomKeyword()
        self.txtContent.setPlainText('Hello, Client!\n請選擇想要的功能')

    def inGuiEvent(self):
        #self.btnGenerate.clicked.connect(self.generateRaw)
        self.btnSearch.clicked.connect(self.plainSearch2)
        #self.btnIndex.clicked.connect(self.generateIndex)
        self.lstTitle.currentRowChanged.connect(self.display2)
        self.btnDecrypt.clicked.connect(self.showPassForm)
        self.spinBox.valueChanged.connect(self.spinValueChanged)
        self.btnSafeSearch.clicked.connect(self.UDMRS)
        self.btnTrapdoor.clicked.connect(self.GenTrapdoor)
        self.btnTrapdoor_2.clicked.connect(self.GenTrapdoor_E)
        self.btnTrapdoorSearch.clicked.connect(self.BDMRS)
        self.btnTrapdoorSearch_2.clicked.connect(self.EDMRS)


    def randomKeyword(self):
        chosen_keyword = random.choices(self.keyword, k = 5)
        texts = ['title','content','push','all']
        search_text = ""
        for keyword in chosen_keyword:
            text = random.choice(texts)
            search_text += f"{keyword}:{text} "
        search_text = search_text[:-1]
        self.txtKeyword.setText(search_text)


    def createDatabase(self):
        f = open(f"index.json", "r")
        str1 = f.read()
        obj = json.loads(str1)
        for i in range(self.num):
            try:
                index = obj[str(i)]
            except:
                continue
            for ind in index:
                self.database[i][ind] = 1


        f.close()

        f = open(f"keyword.txt", "r")
        first = f.read()
        f.close()
        keywords = first.split('\n')
        self.keyword = keywords[:-1]


    def DestroyDialog(self):
        if self.dialog:
            self.dialog.close()

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
        btn.clicked.connect(self.DecryptData)

        self.dialog.setWindowTitle("請輸入密碼")

        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.exec_()

    def DecryptData(self):

        password = self.dialog.edit.text()
        self.dialog.close()
        try:
            key = PBKDF2(password, salt, dkLen=32)
        except:
            return

        if self.searchMode == 1:


            self.searchMode = 99
            plain = []
            title = []

            for result in self.searchResult:
                try:

                    iv = result[0:16]
                    cipheredData = result[16:]
                    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                    originalData = cipher.decrypt(cipheredData)
                    plain.append(originalData.decode())
                    text = plain[-1].split('\n')[1]
                    text = text.split('標題')[1].split('時間')[-2]
                    title.append(text)

                except:

                    plain.append('Decoding Error')
                    title.append('未知的文件')


            self.lstTitle.clear()
            for t in title:

                self.lstTitle.addItem(t)

            self.lstTitle.setCurrentRow(0)

            self.searchResult = plain
            self.searchMode = 3
            if self.searchResult:
                self.display2(0)

        else:
            self.dialog = myDialog()
            self.dialog.resize(713, 300)
            self.dialog.setWindowIcon(QtGui.QIcon(iconFile))

            self.dialog.label = QLabel(self.dialog)
            self.dialog.label.resize(531,41)
            self.dialog.label.move(80,100)
            self.dialog.label.setFont(QFont("Agency FB",24,QFont.Bold))
            self.dialog.label.setText('沒有需要解密的搜尋結果。')


            btn= QPushButton('確定',self.dialog)
            btn.move(260,220)
            btn.resize(160,61)
            btn.clicked.connect(self.DestroyDialog)

            self.dialog.setWindowTitle("錯誤")

            self.dialog.setWindowModality(Qt.ApplicationModal)
            self.dialog.exec_()


    def RScore(self, Du, Q):
        return np.dot(Du, Q)

    def GDFS(self, Nodes, index , Q, RList):
        kthscore = RList[-1][0]

        u = Nodes[index]
        if u.FID == 0:
            if self.RScore(u.D, Q) > kthscore:
                if u.PL != None:
                    self.GDFS(Nodes, u.PL, Q, RList)

                if u.PR != None:
                    self.GDFS(Nodes, u.PR, Q, RList)

            else:
                return

        else:
            score = self.RScore(u.D, Q)
            if score > kthscore:
                for r in RList:
                    if r[1] == u.FID:
                        return

                RList[-1] = (score, u.FID)

                for i in range(len(RList) - 1, 0, -1):
                    if RList[i][0] > RList[i - 1][0]:
                        temp = RList[i - 1]
                        RList[i - 1] = RList[i]
                        RList[i] = temp


            return



    def GenTrapdoor(self):
        currentTime = time.time()
        if not os.path.isfile('dataowner/BDMRStree.json') or not os.path.isfile('dataowner/idf.json'):
            self.txtContent.setPlainText('相關的索引檔尚未建立，請聯絡資料庫擁有者')

            return

        if not os.path.isfile('dataowner/basic_secret.bin'):
            self.txtContent.setPlainText('請先向資料庫擁有者取得金鑰！')
            return

        print('Generate Trapdoor for BDMRS')

        f = open('dataowner/idf.json', 'r')
        str1 = f.read()
        IDF_p = json.loads(str1)

        raw_search = self.txtKeyword.text()

        try:
            search = raw_search.split('->')[0]
            filename = raw_search.split('->')[1]
        except:
            search = raw_search
            filename = 'trapdoor'
        vector = self.getplainSearchVector(search)

        Q = np.zeros(self.m)
        Q_1 = np.zeros(self.m)
        Q_2 = np.zeros(self.m)
        cryptogen = SystemRandom()

        f = open('dataowner/basic_secret.bin', "rb")
        cipherdata = f.read()
        f.close()
        cipherdata = cipherdata.decode()
        cipher = cipherdata.split('\n')
        S = cipher[0]
        index1 = int(cipher[1])
        index2 = int(cipher[2])
        print(cipher)
        M1 = make_spd_matrix(self.m, random_state = index1)
        M2 = make_spd_matrix(self.m, random_state = index2)
        M1_inv = np.linalg.inv(M1)
        M2_inv = np.linalg.inv(M2)

        for i in range(len(vector)):
            if vector[i] != 0:
                Q[i] = IDF_p[i]

        q = math.sqrt(np.sum(np.power(Q, 2)))

        Q = Q / q

        for i in range(self.m):
            if S[i] == '1':
                Q_1[i] = Q[i]
                Q_2[i] = Q[i]
            else:
                Q_1[i] = cryptogen.random()
                Q_2[i] = Q[i] - Q_1[i]

        TD_1 = M1_inv.dot(Q_1)
        TD_2 = M2_inv.dot(Q_2)

        TD = list(TD_1) + list(TD_2)

        used_time = time.time() - currentTime
        print(f'花費時間:{used_time}秒')

        self.txtContent.setPlainText('trapdoor已建立成功')
        f = open(f"trapdoor/BDMRS/{filename}.json", "w")
        f.write(json.dumps(TD))
        f.close()

    def GenTrapdoor_E(self):
        currentTime = time.time()
        if not os.path.isfile('dataowner/EDMRStree.json') or not os.path.isfile('dataowner/idf.json'):
            self.txtContent.setPlainText('相關的索引檔尚未建立，請聯絡資料庫擁有者')

            return

        if not os.path.isfile('dataowner/basic_secret_EDMRS.bin'):
            self.txtContent.setPlainText('請先向資料庫擁有者取得金鑰！')
            return

        print('Generate Trapdoor for EDMRS')

        f = open('dataowner/idf.json', 'r')
        str1 = f.read()
        IDF_p = json.loads(str1)

        raw_search = self.txtKeyword.text()

        try:
            search = raw_search.split('->')[0]
            filename = raw_search.split('->')[1]
        except:
            search = raw_search
            filename = 'trapdoor'
        vector = self.getplainSearchVector(search)

        Q = np.zeros(self.m + self.m_p)
        Q_1 = np.zeros(self.m + self.m_p)
        Q_2 = np.zeros(self.m + self.m_p)
        cryptogen = SystemRandom()

        f = open('dataowner/basic_secret_EDMRS.bin', "rb")
        cipherdata = f.read()
        f.close()
        cipherdata = cipherdata.decode()
        cipher = cipherdata.split('\n')
        S = cipher[0]
        index1 = int(cipher[1])
        index2 = int(cipher[2])
        print(cipher)
        M1 = make_spd_matrix(self.m + self.m_p, random_state = index1)
        M2 = make_spd_matrix(self.m + self.m_p, random_state = index2)
        M1_inv = np.linalg.inv(M1)
        M2_inv = np.linalg.inv(M2)

        for i in range(len(vector)):
            if vector[i] != 0:
                Q[i] = IDF_p[i]


        q = math.sqrt(np.sum(np.power(Q, 2)))

        Q = Q / q

        # Set half of m_p as 1
        Q[np.random.choice(self.m_p, int(self.m_p / 2), replace=False) + self.m] = 1

        for i in range(self.m):
            if S[i] == '1':
                Q_1[i] = Q[i]
                Q_2[i] = Q[i]
            else:
                Q_1[i] = cryptogen.random()
                Q_2[i] = Q[i] - Q_1[i]

        TD_1 = M1_inv.dot(Q_1)
        TD_2 = M2_inv.dot(Q_2)

        TD = list(TD_1) + list(TD_2)

        used_time = time.time() - currentTime
        print(f'花費時間:{used_time}秒')

        self.txtContent.setPlainText('trapdoor已建立成功')
        f = open(f"trapdoor/EDMRS/{filename}.json", "w")
        f.write(json.dumps(TD))
        f.close()



    def BDMRS(self):
        currentTime = time.time()
        self.searchMode = 0


        if not os.path.isfile('dataowner/BDMRStree.json'):
            self.txtContent.setPlainText('相關的索引檔尚未建立，請聯絡資料庫擁有者')
            return

        filename = self.txtKeyword.text()
        if filename == '':
            filename = 'trapdoor'

        if not os.path.isfile(f'trapdoor/BDMRS/{filename}.json'):
            self.txtContent.setPlainText('請先產生搜尋用的trapdoor!')
            return

        print('searching by BDMRS')

        f = open(f"dataowner/BDMRStree.json", "r")
        str1 = f.read()

        n = self.end - self.start + 1
        Nodes = []
        AllNodes = json.loads(str1)
        for Node in AllNodes:
            treenode = TreeNode(Node['ID'], Node['FID'])
            treenode.PL = Node['PL']
            treenode.PR = Node['PR']
            treenode.D = np.array(Node['Iu'])

            Nodes.append(treenode)

        f = open(f'trapdoor/BDMRS/{filename}.json', "r")
        str1 = f.read()
        TD = np.array(json.loads(str1))
        k = self.maxSearchTerm
        RList = [(0, -1) for x in range(k)]
        self.GDFS(Nodes, -1, TD, RList)

        self.searchResult.clear()
        self.lstTitle.clear()

        n = 0
        for ret in RList:
            if ret[1] == -1:
                continue
            n = n + 1

            r = self.start + ret[1]
            f = open(f"dataowner/Encrypted/{r}.bin", "rb")
            context = f.read()
            f.close()
            self.searchResult.append(context)
            self.lstTitle.addItem(f'Encrypted Doc {n}')

        used_time = time.time() - currentTime
        print(f'花費時間:{used_time}秒')
        self.lstTitle.setCurrentRow(0)
        self.searchMode = 1

        if self.searchResult:
            self.display2(0)

    def EDMRS(self):
        currentTime = time.time()
        self.searchMode = 0


        if not os.path.isfile('dataowner/EDMRStree.json'):
            self.txtContent.setPlainText('相關的索引檔尚未建立，請聯絡資料庫擁有者')
            return

        filename = self.txtKeyword.text()
        if filename == '':
            filename = 'trapdoor'

        if not os.path.isfile(f'trapdoor/EDMRS/{filename}.json'):
            self.txtContent.setPlainText('請先產生搜尋用的trapdoor!')
            return

        print('searching by EDMRS')

        f = open(f"dataowner/EDMRStree.json", "r")
        str1 = f.read()

        n = self.end - self.start + 1
        Nodes = []
        AllNodes = json.loads(str1)
        for Node in AllNodes:
            treenode = TreeNode(Node['ID'], Node['FID'])
            treenode.PL = Node['PL']
            treenode.PR = Node['PR']
            treenode.D = np.array(Node['Iu'])

            Nodes.append(treenode)

        f = open(f'trapdoor/EDMRS/{filename}.json', "r")
        str1 = f.read()
        TD = np.array(json.loads(str1))
        k = self.maxSearchTerm
        RList = [(0, -1) for x in range(k)]
        self.GDFS(Nodes, -1, TD, RList)

        self.searchResult.clear()
        self.lstTitle.clear()

        n = 0
        for ret in RList:
            if ret[1] == -1:
                continue
            n = n + 1

            r = self.start + ret[1]
            f = open(f"dataowner/Encrypted/{r}.bin", "rb")
            context = f.read()
            f.close()
            self.searchResult.append(context)
            self.lstTitle.addItem(f'Encrypted Doc {n}')

        used_time = time.time() - currentTime
        print(f'花費時間:{used_time}秒')
        self.lstTitle.setCurrentRow(0)
        self.searchMode = 1

        if self.searchResult:
            self.display2(0)


    def UDMRS(self):
        currentTime = time.time()
        self.searchMode = 0
        print('searching by UDMRS')

        if not os.path.isfile('dataowner/plaintree.json') or not os.path.isfile('dataowner/idf.json'):
            print('相關的索引檔尚未建立，請聯絡資料庫擁有者')
            return

        f = open(f"dataowner/plaintree.json", "r")
        str1 = f.read()

        n = self.end - self.start + 1
        Nodes = []
        AllNodes = json.loads(str1)
        for Node in AllNodes:
            treenode = TreeNode(Node['ID'], Node['FID'])
            treenode.PL = Node['PL']
            treenode.PR = Node['PR']
            treenode.D = np.array(Node['D'])

            Nodes.append(treenode)


        f = open('dataowner/idf.json', 'r')
        str1 = f.read()
        IDF_p = json.loads(str1)

        search = self.txtKeyword.text()
        vector = self.getplainSearchVector(search)

        Q = np.zeros(1500)

        for i in range(len(vector)):
            if vector[i] != 0:
                Q[i] = IDF_p[i]

        q = math.sqrt(np.sum(np.power(Q, 2)))

        Q = Q / q

        print(self.RScore(Nodes[0].D, Q))

        k = self.maxSearchTerm

        RList = [(0, -1) for x in range(k)]

        self.GDFS(Nodes, -1, Q, RList)

        print(RList)


        self.searchResult.clear()
        self.lstTitle.clear()

        n = 0
        for ret in RList:
            if ret[1] == -1:
                continue
            n = n + 1

            r = self.start + ret[1]
            f = open(f"dataowner/Encrypted/{r}.bin", "rb")
            context = f.read()
            f.close()
            self.searchResult.append(context)
            self.lstTitle.addItem(f'Encrypted Doc {n}')

        used_time = time.time() - currentTime
        print(f'花費時間:{used_time}秒')
        self.lstTitle.setCurrentRow(0)
        self.searchMode = 1

        if self.searchResult:
            self.display2(0)





    def spinValueChanged(self):
        self.maxSearchTerm = self.spinBox.value()


    def display(self, currentRow):
        if self.lstTitle.count == 0:
            return

        if self.searchMode == 1:
            j_content = self.searchResult[currentRow]['content'].split('※ 發信站: 批踢踢實業坊')[0]
            try:
                j_title =j_content.split('\n')[1]
                j_content = j_content.split(j_title)[1]
                j_title = self.searchResult[currentRow]['title']
            except:
                j_title = ''
            try:
                j_push = self.searchResult[currentRow]['content'].split('※ 發信站: 批踢踢實業坊')[1]
            except:
                j_push = ''

            content = '-----TITLE------\n'
            content = content + j_title + '\n'
            content = content + '-----CONTENT-----\n'
            content = content + j_content + '\n'
            content = content + '-----PUSH-----\n'
            content = content + j_push
            self.txtContent.setPlainText(content)


    def display2(self, currentRow):
        if self.lstTitle.count == 0:
            return

        if self.searchMode == 1:
            cp = '------ENCRYPTED DOC------\n'
            cp += b64encode(self.searchResult[currentRow]).decode('utf-8')
            self.txtContent.setPlainText(cp)

        elif self.searchMode == 2:
            j_content = self.searchResult[currentRow]['content'].split('※ 發信站: 批踢踢實業坊')[0]
            try:
                j_title =j_content.split('\n')[1]
                j_content = j_content.split(j_title)[1]

            except:
                j_title = ''
            try:
                j_push = self.searchResult[currentRow]['content'].split('※ 發信站: 批踢踢實業坊')[1]
            except:
                j_push = ''

            content = '-----TITLE------\n'
            content = content + j_title + '\n'
            content = content + '-----CONTENT-----\n'
            content = content + j_content + '\n'
            content = content + '-----PUSH-----\n'
            content = content + j_push
            self.txtContent.setPlainText(content)

        elif self.searchMode == 3:
            content = self.searchResult[currentRow]
            j_content = content.split('※ 發信站: 批踢踢實業坊')[0]
            try:
                j_title = j_content.split('\n')[1]
                j_content = j_content.split(j_title)[1]

            except:
                j_title = ''
            try:
                j_push = content.split('※ 發信站: 批踢踢實業坊')[1]
            except:
                j_push = ''

            content = '-----TITLE------\n'
            content = content + j_title + '\n'
            content = content + '-----CONTENT-----\n'
            content = content + j_content + '\n'
            content = content + '-----PUSH-----\n'
            content = content + j_push
            self.txtContent.setPlainText(content)


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

            for keyword in self.keyword:
                if keyword in j['title']:
                    title.append(count)

                j_content = j['content'].split('※ 發信站: 批踢踢實業坊')[0]
                try:
                    j_push = j['content'].split('※ 發信站: 批踢踢實業坊')[1]
                except:
                    j_push = ''

                try:
                    j_title = j_content.split('\n')[1]
                    j_content = j_content.split(j_title)[1]
                except:
                    pass

                if keyword in j_content:
                    content.append(count + 500)

                if keyword in j_push:
                    push.append(count + 1000)

                count = count + 1


            title.extend(content)
            title.extend(push)
            database[i] = title

        f = open(f"index.json", "w")
        f.write(json.dumps(database))
        f.close()



    def generateRaw(self):
        counter = 67532
        print("從PTT抓取資料中...")

        #2000 - 3866 #16000 - 17577
        for i in range(14000, 16000):
            try:
                print(f'Processing page {i}...')
                url=f'https://www.ptt.cc/bbs/C_Chat/index{i}.html'
                page = requests.get(url).text
                htm = soup(page,'html.parser')
                result = htm.select("div.title a")

                msg = ""
                self.txtContent.setPlainText("")
                for i, r in enumerate(result):
                    obj = {}
                    msg = ""
                    msg += r.text + "\n"
                    obj['title'] = r.text

                    f = open(f"rawText/{counter}.json", "w")
                    #msg += r['href'] + "\n"
                    article_url = 'https://www.ptt.cc/' + r['href']
                    article = requests.get(article_url).text

                    content = soup(article,'html.parser')
                    msg = ""
                    content_result = content.select('div#main-container')
                    for c in content_result:
                        msg += c.text + "\n"

                    obj['content']= msg

                    push_result = content.select('div.push')
                    msg = ""
                    for p in push_result:

                        msg += p.select('span.push-userid')[0].text
                        msg += p.select('span.push-content')[0].text + "\n"

                    obj['push'] = msg


                    f.write(json.dumps(obj))
                    f.close()
                    counter += 1
                    self.txtContent.setPlainText(self.txtContent.toPlainText()+f"Processed Article {'https://www.ptt.cc/' + r['href']}\n")
                self.txtContent.setPlainText(self.txtContent.toPlainText()+f"Processed Page{i}\n")
            except:
                pass

    def getplainSearchVector(self, search):
        keywords = search.split(' ')
        vector = np.zeros((1500))
        for keyword in keywords:
            name = keyword.split(':')[0]
            Type = keyword.split(':')[1]

            if name in self.keyword:
                index = self.keyword.index(name)

                if Type == 'title':
                    print(index)
                    vector[index] = 1

                elif Type == 'content':
                    vector[index + 500] = 1
                    print(index + 500)
                elif Type == 'push':
                    print(index + 1000)
                    vector[index + 1000] = 1

                elif Type == 'all':
                    vector[index] = 1
                    vector[index + 500] = 1
                    vector[index + 1000] = 1

        return vector




    def plainSearch(self):
        self.searchMode = 0
        self.txtContent.setPlainText(f"對原始資料進行搜尋... ({self.txtKeyword.text()})")
        search = self.txtKeyword.text()
        vector = getplainSearchVector(search)
        result = np.dot(self.database, vector)

        print('sum')
        print(np.sum(result))
        rank = (np.argsort(result))[::-1]
        print(rank)
        final_rank = [x for x in rank if result[x] > 0]
        final_rank = final_rank[:self.maxSearchTerm]

        print(len(final_rank))



        self.searchResult.clear()
        self.lstTitle.clear()

        for ret in final_rank:
            f = open(f"dataowner/rawText/{ret}.json", "r")
            context = f.read()
            f.close()
            j = json.loads(context)
            self.searchResult.append(j)
            self.lstTitle.addItem(j['title'])

        self.lstTitle.setCurrentRow(0)
        self.searchMode = 1

        if self.searchResult:
            self.display(0)


    def plainSearch2(self):
        self.searchMode = 0
        self.txtContent.setPlainText(f"對原始資料進行搜尋... ({self.txtKeyword.text()})")
        search = self.txtKeyword.text()
        keywords = search.split(' ')
        vector = np.zeros((1500))
        for keyword in keywords:
            name = keyword.split(':')[0]
            Type = keyword.split(':')[1]

            if name in self.keyword:
                index = self.keyword.index(name)

                if Type == 'title':
                    print(index)
                    vector[index] = 1

                elif Type == 'content':
                    vector[index + 500] = 1
                    print(index + 500)
                elif Type == 'push':
                    print(index + 1000)
                    vector[index + 1000] = 1

                elif Type == 'all':
                    vector[index] = 1
                    vector[index + 500] = 1
                    vector[index + 1000] = 1


        result = np.dot(self.database, vector)

        print('sum')
        print(np.sum(result))
        rank = (np.argsort(result))[::-1]
        print(rank)
        final_rank = [x for x in rank if result[x] > 0]
        final_rank = final_rank[:self.maxSearchTerm]

        print(len(final_rank))



        self.searchResult.clear()
        self.lstTitle.clear()

        n = 0
        for ret in final_rank:
            n = n + 1
            f = open(f"dataowner/Encrypted/{ret}.bin", "rb")
            context = f.read()
            f.close()
            self.searchResult.append(context)
            self.lstTitle.addItem(f'Encrypted Doc {n}')

        self.lstTitle.setCurrentRow(0)
        self.searchMode = 1

        if self.searchResult:
            self.display2(0)




       # print(search)
        #index = self.keyword.index(search)
        #print(index)




