# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:10:22 2020

@author: user
"""


from PyQt5 import QtWidgets
from mainForm.core import MainUi
import sys

    
if __name__ == "__main__":
    def run_app():
        app = QtWidgets.QApplication(sys.argv)
        window = MainUi()
        window.show()
        app.exec_()
    run_app()