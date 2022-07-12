# 数独游戏

舞蹈链实现的数独游戏

* 环境python3,pyqt5
* 使用了舞蹈链
* 具有提示、选择难度等功能
* 有游戏失败等功能的坑等待填。。。玩还是还可以玩

主要代码在 sudokucore.py、DLXWindow.py中，其中sudokucore.py主要为舞蹈链编写以及数独的核心逻辑，DLXWindow.py主要为界面的编写。想要知道具体实现的讲解可以看：

* [python 舞蹈链数独游戏](https://zhou-ning.github.io/2022/07/11/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/python%E8%88%9E%E8%B9%88%E9%93%BE%E6%95%B0%E7%8B%AC%E6%B8%B8%E6%88%8F/)
* [python 舞蹈链数独游戏](https://blog.csdn.net/qq_41474648/article/details/125746862?spm=1001.2014.3001.5501)

界面：

![image-20200722221752967](https://cdn.jsdelivr.net/gh/zhou-ning/blog-image-bed@main/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/image-20220712162658587.png)

难度使用读取txt进行，分别对应着简单.txt、普通.txt、困难.txt。
