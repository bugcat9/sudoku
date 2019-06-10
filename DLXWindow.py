
import sys
import sudokucore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import copy

class SudokuWindow(QMainWindow):
    def __init__(self):
        super().__init__()       
        self.mysudokucore=sudokucore.sudokucore()
        self.choosenum=-1
        self.count=0
        self.timecount=60
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)
        self.time.start()
        
        self.revocationLeftList=[]
        self.revocationRightList=[]
        self.initUI()
        self.tip=()
       
    def initUI(self): 
        self.setWindowTitle("数独")
        self.setFixedSize(700,630)
        self.setStyleSheet('QMainWindow{background-color:  #E8E8E8}')
        menubar = self.menuBar()
        LevelBar=menubar.addMenu('Level')
        
        Level1Action = QAction( 'Level1', self)      
        Level2Action = QAction( 'Level2', self) 
        Level1Action.triggered.connect(self.chooseLevel1)    
        Level2Action.triggered.connect(self.chooseLevel2) 
        
        LevelBar.addAction(Level1Action)
        
        LevelBar.addAction(Level2Action)
        
        self.LevelLabel=QLabel(self)
        self.LevelLabel.move(0,40)
        self.LevelLabel.resize(160,30)
        self.LevelLabel.setText('Level  1')
        self.LevelLabel.setStyleSheet('QLabel{color:rgb(300,300,300,120);font-size:23px;font-weight:bold;font-family:宋体;text-align:center;}')
        
        label=QLabel(self)
        label.move(140,40)
        label.resize(50,50)
        label.setStyleSheet('QLabel{border-image: url(image/8.ico)}')
        self.timerLabel=QLabel(self)
        self.timerLabel.setStyleSheet('QLabel{background:white;color:rgb(300,300,300,120);font-size:20px;font-weight:bold;font-family:宋体;text-align:center;}')
        self.timerLabel.setText('00:00:60')
        self.timerLabel.move(200,50)
        
        self.ButtonList=[QPushButton(self)   for i in range(8)]
        for i in range(8):
            self.ButtonList[i].resize(40,40)
            self.ButtonList[i].move(320+i*40,40)
        
        self.ButtonList[0].setStyleSheet('QPushButton{border-image: url(image/0.ico)}'
                                                                            'QPushButton:pressed{border-image: url(image/0.ico);border-style: outset;background-color: #33CCFF}')
        self.ButtonList[1].setStyleSheet('QPushButton{border-image: url(image/1.ico)}'
                                                                             'QPushButton:pressed{border-image: url(imge/1.ico);border-style: outset;background-color: #33CCFF}')
        self.ButtonList[2].setStyleSheet('QPushButton{border-image: url(image/2.ico)}'
                                                                             'QPushButton:pressed{border-image: url(imge/2.ico);border-style: outset;background-color: #33CCFF}')
        self.ButtonList[3].setStyleSheet('QPushButton{border-image: url(image/3.ico)}'
                                                                             'QPushButton:pressed{border-image: url(imge/3.ico);border-style: outset;background-color: #33CCFF}')
        self.ButtonList[4].setStyleSheet('QPushButton{border-image: url(image/4.ico)}'
                                                                             'QPushButton:pressed{border-image: url(imge/4.ico);border-style: outset;background-color: #33CCFF}')    
        self.ButtonList[5].setStyleSheet('QPushButton{border-image: url(image/5.ico)}'
                                                                             'QPushButton:pressed{border-image: url(imge/5.ico);border-style: outset;background-color: #33CCFF}')
        self.ButtonList[6].setStyleSheet('QPushButton{border-image: url(image/6.ico)}'
                                                                             'QPushButton:pressed{border-image: url(imge/6.ico);border-style: outset;background-color: #33CCFF}')
        self.ButtonList[7].setStyleSheet('QPushButton{border-image: url(image/7.ico)}'
                                                                             'QPushButton:pressed{border-image: url(imge/7.ico);border-style: outset;background-color: #33CCFF}')

        self.ButtonList[0].clicked.connect(self.eraser)
        self.ButtonList[1].clicked.connect(self.Restart)
        self.ButtonList[2].clicked.connect(self.reset)
        self.ButtonList[3].clicked.connect(self.Stop)
        self.ButtonList[4].clicked.connect(self.getTip)
        self.ButtonList[5].clicked.connect(self.revocationLeft)
        self.ButtonList[6].clicked.connect(self.revocationRight)
        self.ButtonList[7].clicked.connect(self.recharge)
        
    def chooseLevel1(self):
        self.mysudokucore.LevelFile=self.mysudokucore.Leveldict[1]
        self.mysudokucore.initMaze()
        self.LevelLabel.setText('Level  1')
        self.update()
    
    def chooseLevel2(self):
        self.mysudokucore.LevelFile=self.mysudokucore.Leveldict[2]
        self.mysudokucore.initMaze()
        self.LevelLabel.setText('Level  2')
        self.update()
    
    #清除函数
    def eraser(self):
        self.choosenum=0
        pixmap=QPixmap ('image/0.png')
        cursor =QCursor(pixmap,-1,-1) 
        self.setCursor(cursor)
    
    def Restart(self):
        self.mysudokucore.Restartgame()
        self.choosenum=-1
        self.update()
        self.unsetCursor()
    def revocationLeft(self):
        if len(self.revocationLeftList)!=0:    
            t=self.revocationLeftList.pop()
            self.revocationRightList.append((t[0],t[1], self.mysudokucore[t[0]][t[1]]))
            self.mysudokucore[t[0]][t[1]]=t[2]
        self.update()
        self.unsetCursor()
    def revocationRight(self):
        if len(self.revocationRightList)!=0:    
            t=self.revocationRightList.pop()
            self.revocationLeftList.append((t[0],t[1], self.mysudokucore[t[0]][t[1]]))
            self.mysudokucore[t[0]][t[1]]=t[2]
        self.update()
    def reset(self):
        self.mysudokucore.reset()
        self.choosenum=-1
        self.update()
        self.unsetCursor()
    def recharge(self):
        if self.mysudokucore.judge():
            self.mysudokucore.maze=copy.deepcopy(self.mysudokucore.ansMaze)
        self.update()
        self.unsetCursor()
    def getTip(self):

        self.tip=self.mysudokucore.getTip()
        print(self.tip)
        self.update()
        self.unsetCursor()
 
    def Stop(self):
        if  self.time.isActive():
            self.time.stop()
        else:
            if  self.timecount<=0:
                self.timecount=60
            self.time.start()
        self.unsetCursor()
    def  Refresh(self):
        self.timecount-=1
        num='00:00:%d'%self.timecount
        if  self.timecount>=0:
            self.timerLabel.setText(num)
        
    
    
    def paintEvent(self, event):
        painter=QPainter()
        pen=QPen()
        font=QFont()
        
        painter.begin(self)
        painter.fillRect(100,100,450,450,Qt.white)
        pen.setWidth(2)
        painter.setPen(pen)
        #画线
        for i in range(10):
            if i%3==0 and i!=0 and i!=9:
                pen.setColor(Qt.red)
                painter.setPen(pen)
            else:
                pen.setColor(Qt.black)
                painter.setPen(pen)
            painter.drawLine(100,100+i*50,550,100+i*50)   #画横线
            painter.drawLine(100+i*50,100,100+i*50,550)   #画竖线
        
        #画旁边9个选择
        font.setBold(True)
        font.setBold(True)
        font.setFamily("宋体")
        font.setPointSize(25)
        painter.setFont(font)
        #画旁边的数字选择栏
        for i in range(9):
            if self.choosenum==i+1:
                pen.setColor(Qt.magenta)
                painter.setPen(pen)
            else:
                pen.setColor(Qt.black)
                painter.setPen(pen)
            painter.drawRect(600,100+i*50,50,50)
            painter.drawText(600,100+i*50,50,50,Qt.AlignCenter,str(1+i))
        
        pen.setColor(Qt.black)
        painter.setPen(pen)
        #画格子中的数字
        self.count=0
        for i in range(9):
            for j in range(9):
                z=int( self.mysudokucore[i][j])
                if z!=0:
                    self.count+=1
                    if self.mysudokucore.Iscanchangmaze[i][j]:
                        pen.setColor(Qt.black)
                        painter.setPen(pen)
                    else:
                        pen.setColor(Qt.blue)
                        painter.setPen(pen)
                    painter.drawText((j+2)*50,(i+2)*50,50,50,Qt.AlignCenter,str(self.mysudokucore[i][j]))
        
        #画tip
        if self.tip!=():
            pen.setColor(Qt.yellow)
            painter.setPen(pen)
            self.mysudokucore[self.tip[0]][self.tip[1]]=self.tip[2]
            painter.drawText((self.tip[1]+2)*50,(self.tip[0]+2)*50,50,50,Qt.AlignCenter,str(self.mysudokucore[self.tip[0]][self.tip[1]]))
        self.tip=()
        painter.end()
        
        if self.count==81  and  self.mysudokucore.maze==self.mysudokucore.ansMaze:
            self.mysudokucore.ansMaze=[]
            QMessageBox.information(self, '恭喜', '挑战成功' )
    
        
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton :
            print(event.x()//50,event.y()//50)
            x=event.x()//50
            y=event.y()//50
            
            if 2<=x<=10 and 2<=y<=10:
                if self.choosenum!=-1 and self.mysudokucore.Iscanchangmaze[y-2][x-2]:
                    self.revocationLeftList.append((y-2,x-2,self.mysudokucore[y-2][x-2]))
                    self.mysudokucore[y-2][x-2]=self.choosenum
                    if self.mysudokucore.judge():
                        print("正确")
                        for i in self.mysudokucore.maze:
                            print(i)
                        print("1111111111111111111")
                        for i in self.mysudokucore.ansMaze:
                            print(i)
                    else:
                        print("错了")
            elif x==12 and 2<=y<=10:
                self.choosenum=y-1
                self.unsetCursor()
            else:
                self.choosenum=-1
                self.unsetCursor()
        
        self.update()
if __name__ == '__main__':
     
    app = QApplication(sys.argv)
    ex = SudokuWindow()
    ex.show()
    sys.exit(app.exec_())