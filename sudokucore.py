
import random
import copy
from _operator import index
import time
from turtledemo.penrose import star



# 舞蹈链的结点
class DLXNode:
    def __init__(self, row=-1, col=-1):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.colHead = self

        # 用于列头，记录结点数
        self.count = 0
        # 单纯的标记，方便调试
        self.colId = col
        self.rowId = row


class DLX:
    def __init__(self, colnum):
        """舞蹈链初始化
        args:
            colnum:链表头个数
        """
        # self.count = 0
        # 行数
        self.rownum = 0
        # 记录行字典
        self.rowdict = {}
        self.ans = []
        self.head = DLXNode()
        self.col = [DLXNode(-1, i) for i in range(colnum)]

        # 将链表头和head连接起来
        self.head.left = self.col[-1]
        self.head.right = self.col[0]
        self.col[0].left = self.head
        self.col[0].right = self.col[1]
        self.col[-1].left = self.col[-2]
        self.col[-1].right = self.head
        # 将链表头之间连接起来
        for i in range(1, colnum-1):
            self.col[i].left = self.col[i-1]
            self.col[i].right = self.col[i+1]

    def pushRow(self, colList):
        """插入一行数据，按照一行一行，递增的插入
        args:
            colList:数组，里面存着列头的id
        """
    
        # print(colList,self.rownum)
        self.rowdict[self.rownum] = colList

        # 对于结点，列方向上，上下指针的变动
        for cowId in colList:
            # 每个插入的结点，都为该列最后一个结点
            node = DLXNode(self.rownum, cowId)
            node.down = self.col[cowId]
            node.up = self.col[cowId].up
            node.colHead = self.col[cowId]
            self.col[cowId].up.down = node
            self.col[cowId].up = node

            self.col[cowId].count += 1

        # 对于结点，行方向的两个指针的变动
        for i in range(len(colList)):
            self.col[colList[i]].up.left = self.col[colList[i-1]].up
            self.col[colList[i]].up.right = self.col[colList[(i+1) % len(colList)]].up

        self.rownum += 1

    def remove(self, c: DLXNode):
        """以列为单位进行删除
        args:
            c:列头
        return:
            删除是否成功的结果
        """
        # print(c.colId,'列被删除')
        # 将列头从链表头中删除，只改变了c结点left、right的指向，并未改变c的指向，为恢复做准备
        c.left.right = c.right
        c.right.left = c.left
        if c.down == c:
            return False
        i = c.down
        while i != c:
            #遍历这一列，i为这一列中的结点
            #注意，遍历了这一列，但是并没有改变这一列结点之间的关系，为后面的恢复埋下了种子
            j = i.right
            while j != i:
                # 遍历i结点这一行，将这一行的结点进行删除
                # 注意只是改变了j结点up、down的指向，并没有改变j的指向，为后面j的恢复做准备
                j.up.down = j.down
                j.down.up = j.up
                j.colHead.count -= 1
                j = j.right
            i = i.down
        return True

    def recover(self, c: DLXNode):        
        """以列为单位进行恢复
        args:
            c:列头
        return:
            恢复是否成功的结果
        """
        # print(c.colId,'列被恢复')
        i = c.down
        while i != c:
            #遍历这一列，i为这一列结点
            j = i.right
            while j != i:
                # 遍历i结点这一行，根据j结点的指向进行恢复
                j.up.down = j
                j.down.up = j
                j.colHead.count += 1
                j = j.right
            i = i.down
        # 根据c结点的指向，将c加入到链表头当中
        c.left.right = c
        c.right.left = c

    # 寻找count最小的
    def FindMinCount(self):
        c = self.head.right
        minnode = c
        while c != self.head:
            if c.count < minnode.count:
                minnode = c
            c = c.right
        return minnode

    def Dance(self):
        # 寻找结点数最少的列
        c = self.FindMinCount()
        if c == self.head:
            return True
        
        # 删除结点数最少的列c
        if not self.remove(c):
            # print('删除失败')
            self.recover(c)
            # self.count-=1
            return False
        
        i = c.down
        while i != c:
            # 选择第i行为答案，需要将第i行上结点的列进行删除
            # print((i.rowId,i.colId),self.count)
            j = i.right
            while j != i:
                self.remove(j.colHead)
                j = j.right

            if self.Dance():
                # print("跳舞成功")
                self.ans.append(self.rowdict[i.rowId])
                return True

            # 进行回溯
            j = i.right
            while j != i:
                self.recover(j.colHead)
                j = j.right
            i = i.down

        # self.count-=1
        # 恢复被删除的列c
        self.recover(c)
        return False


class sudoku(DLX):
    def __init__(self, maze):
        """
        args:
            maze:大小9*9，内容为每个单元格填写的数字
        """
        super().__init__(9*9*4)
        # 切断关系采取深复制
        self.maze = copy.deepcopy(maze)

    def pushToDLX(self):
        for x in range(9):
            for y in range(9):
                z = int(self.maze[x][y])
                colList = []
                if z != 0:
                    # 单元格有数字
                    N1 = x*9+y
                    N2 = x*9+z+80
                    N3 = y*9+z+161
                    N4 = ((x//3)*3+(y//3))*9+z+242
                    colList.append(N1)
                    colList.append(N2)
                    colList.append(N3)
                    colList.append(N4)
                    self.pushRow(colList)
                else:
                    # 单元格没有数字，将9种可能性都插入
                    for i in range(1, 10):
                        colList = []
                        z = i
                        N1 = x*9+y
                        N2 = x*9+z+80
                        N3 = y*9+z+161
                        N4 = ((x//3)*3+(y//3))*9+z+242
                        colList.append(N1)
                        colList.append(N2)
                        colList.append(N3)
                        colList.append(N4)
                        self.pushRow(colList)

    def initalRmove(self):
        for x in range(9):
            for y in range(9):
                z = int(self.maze[x][y])
                if z != 0:
                    N1 = x*9+y
                    N2 = x*9+z+80
                    N3 = y*9+z+161
                    N4 = ((x//3)*3+(y//3))*9+z+242
                    self.remove(self.col[N1])
                    self.remove(self.col[N2])
                    self.remove(self.col[N3])
                    self.remove(self.col[N4])

    def IsCanDance(self):
        self.pushToDLX()
        self.initalRmove()
        if self.Dance():
            return True
        else:
            return False

    def ans2Maze(self):
        for col in self.ans:
            x = col[0]//9
            y = col[0] % 9
            z = (col[1]-80) % 9
            if z == 0:
                z = 9
            self.maze[x][y] = z


class sudokucore():
    def __init__(self):
        self.Iscanchangmaze = [[True]*9 for i in range(9)]
        self.randomList = [i for i in range(1, 10)]
        # levelfile 保存着初盘数组
        self.LevelFile = '困难.txt'
        self.initMaze()

        self.Leveldict = dict()
        self.Leveldict[1] = '简单.txt'
        self.Leveldict[2] = '普通.txt'
        self.Leveldict[3] = '困难.txt'
        print(self.Iscanchangmaze)

    def initMaze(self):

        self.maze = []
        with open(self.LevelFile, 'r') as f:
            for line in f.readlines():
                self.maze.append(line.strip().split(','))
        # 进行洗牌
        random.shuffle(self.randomList)
        print(self.randomList)
        self.colDict = {}
        for i in range(9):
            self.colDict[self.randomList[i]] = i
        # 进行变换
        print(self.colDict)
        for i in range(9):
            for j in range(9):
                z = int(self.maze[i][j])
                if z != 0:
                    index = self.colDict[z]
                    # 对应的数字进行变换
                    self.maze[i][j] = self.randomList[(index+1) % 9]
                    self.Iscanchangmaze[i][j] = False

    def __getitem__(self, key):
        return self.maze[key]

    def judge(self):
        # print(id(self.maze))
        s = sudoku(self.maze)
        if s.IsCanDance():
            s.ans2Maze()
            self.ansMaze = s.maze[:]
            return True
        else:
            return False
    
    # 开始新的游戏
    def Restartgame(self):
        self.initMaze()
    
    # 重置
    def reset(self):

        self.maze = []
        with open(self.LevelFile, 'r') as f:
            for line in f.readlines():
                self.maze.append(line.strip().split(','))

        # 进行变换
        for i in range(9):
            for j in range(9):
                z = int(self.maze[i][j])
                if z != 0:
                    index = self.colDict[z]
                    self.maze[i][j] = self.randomList[(index+1) % 9]
                    # self.Iscanchangmaze[i][j]=False

    def getTip(self):
        if self.judge():
            for i in range(9):
                for j in range(9):
                    if self.maze[i][j] != self.ansMaze[i][j]:
                        return (i, j, self.ansMaze[i][j])
        else:
            return ()


if __name__ == '__main__':
    start = time.time()
    c = sudokucore()
    if c.judge():
        for i in c.ansMaze:
            print(i)
        print('1111111111111111111111111111111111111111111111111111')
        for i in c.maze:
            print(i)
    print(time.time()-start)
    '''
    #数组的测试
    a=sudoku()
    a.pushToDLX()
    a.initalRmove()
    if not a.Dance():
        print("失败了")
    else:
        print(len(a.ans))
    a.ans2Maze()
    for i in a.maze:
        print(i)
    '''
    '''
    # DLX的测试
    r1=[2,4,5]
    r2=[0,3,6]
    r3=[1,2,5]
    r4=[0,3]
    r5=[1,6]
    r6=[3,4,6]
    b=DLX(7)
    b.pushRow(r1)
    b.pushRow(r2)
    b.pushRow(r3)
    b.pushRow(r4)
    b.pushRow(r5)
    b.pushRow(r6)
    if not b.Dance():
        print("失败了")
    '''
