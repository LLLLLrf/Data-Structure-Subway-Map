# Data-Structure-Subway-Map
This is the assignment of our data structure and algorithm course
## 如何运行程序

1. 在运行前在根目录运行  ``pip install --user -r requirements.txt -i https://pypi.douban.com/simple``  检查是否已安装程序相关依赖

2. 打开`Main.py`，运行程序，程序将自动弹出交互界面

3. 在弹出窗口中进行选择

   a. 查看广州地铁路线图：点击“查看广州地铁路线图”按钮，将自动打开路线图html文件（程序目录下需有`Guangzhou_railway.html`文件）

   b. 查询最短路径/最少换乘次数路径：输入起始地铁站和终点地铁站，然后点击“最短路径”或“最少换乘”按钮，将自动打开推荐路线图html文件

   4.查看查询过的推荐路线图：打开程序所在目录，根据文件名找到对应的推荐路线图




## 如何运行测试

打开`test.py`，运行程序，将自动测试是否广州地铁的任意两条路径都能生成最短路径/最少换乘次数路径并生成html文件，并在终端输出每个测试的结果。
