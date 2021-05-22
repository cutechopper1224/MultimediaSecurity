# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 16:30:15 2019

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
path = os.getcwd()
qtCreatorFile = path + os.sep + "SSE.ui"
iconFile = path + os.sep + "logo.png"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


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
        self.database = np.zeros((self.num, 1500))
        self.keyword = []
        self.maxSearchTerm = 100
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1000) 
        self.spinBox.setValue(100)
        
        self.searchResult = []
        self.searchMode = 0
        self.createDatabase()
        

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


       

    def inGuiEvent(self):
        self.btnGenerate.clicked.connect(self.generateRaw)
        self.btnSearch.clicked.connect(self.plainSearch)
        self.btnIndex.clicked.connect(self.generateIndex)
        self.lstTitle.currentRowChanged.connect(self.display)
        self.spinBox.valueChanged.connect(self.spinValueChanged)
    

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


    def plainSearch(self):
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

        for ret in final_rank:
            f = open(f"rawText/{ret}.json", "r")
            context = f.read()
            f.close()
            j = json.loads(context)
            self.searchResult.append(j)
            self.lstTitle.addItem(j['title'])

        self.lstTitle.setCurrentRow(0)
        self.searchMode = 1
            
        if self.searchResult:
            self.display(0)

        

            
       
       # print(search)
        #index = self.keyword.index(search)
        #print(index)
       
     
        
   