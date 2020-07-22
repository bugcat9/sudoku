# 数独游戏

舞蹈链实现的数独游戏

* 环境python3,pyqt5
* 使用了舞蹈链
* 具有提示、选择难度等功能
* 有游戏失败等功能的坑等待填。。。玩还是还可以玩

主要代码在 sudokucore.py、DLXWindow.py中，其中sudokucore.py主要为舞蹈链编写以及数独的核心逻辑，DLXWindow.py主要为界面的编写。想要知道详细情况可以[访问数独.pdf](/访问数独.pdf)

界面：

![image-20200722221752967](/image-20200722221752967.png)

难度使用读取txt进行，分别对应着简单.txt、普通.txt、困难.txt

其实本来想将其打包，但是由于pyQt的原因没有打包成功，所以多一些乱七八糟的没有用的东西

参考：

* https://www.cnblogs.com/grenet/p/3145800.html
* https://www.cnblogs.com/grenet/p/3163550.html
* https://blog.csdn.net/zj0395/article/details/72773001