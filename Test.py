
'''
Created on 2019年4月30日

@author: zhouning
'''
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *




if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = SudokuWindow()
    ex.show()
    sys.exit(app.exec_())