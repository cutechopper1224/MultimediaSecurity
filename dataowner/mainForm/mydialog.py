# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 14:09:42 2020

@author: user
"""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class myDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.confirmed = False
        self.password = ""
        self.edit = None
    