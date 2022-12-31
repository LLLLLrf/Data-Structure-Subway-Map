import pickle
import os

import TransferTime
import Window
import graphFile
import Shortest
import Map

'''
————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
以下为主运行函数
'''

'''
主运行函数
用于将输入的起点和终点传入函数得到最短路径/最少换乘次数路径，并将路径传入函数以生成路线图
'''


def main(testBool, testMode=None, testStart=None, testEnd=None):
    # 检查当前目录下是否存在广州地铁路线图的pikcle文件,存在则导入以邻接表存储的地铁图(graph),不存在则调用get_graph()函数生成
    if not os.path.exists('./graph.pkl'):
        graph = graphFile.get_graph()
        pklfile = open('graph.pkl', 'wb')
        pickle.dump(graph, pklfile)
        pklfile.close()
    else:
        pklfile = open("graph.pkl", 'rb')
        graph = pickle.load(pklfile)
        pklfile.close()
    ifTest = testBool
    if not ifTest:
        mode = 2
        start, end, mode = Window.interactiveInterface(graph)
    else:
        mode = testMode
        start = testStart
        end = testEnd

    # 根据选择的模式来计算从起点到终点的最短路径/最少换乘次数路径，并生成路线图

    # 运行dijksrta()函数以获得最短路径(shortestPath)和最短路径长度(distance)，并生成路线图
    if mode == 0:
        shortestPath, dis = Shortest.dijksrta(start, end, graph)
        distance = [dis]
        Map.plot(shortestPath, graph, distance, ifTest)

    # 生成地铁线的特殊图，运行dijksrta()函数以获得最少换乘次数路径(linePath)和最少换乘次数，调用getDistance()函数获得路径长度，并生成路线图
    if mode == 1:
        linegraph = TransferTime.get_lineGraph(graph)
        linePath, dis = Shortest.dijksrta(start, end, linegraph)
        transferPath = TransferTime.get_transferPath(linePath)
        distance = [int((dis - 1) / 2), TransferTime.getDistance(transferPath, graph)]
        Map.plot(transferPath, graph, distance, ifTest)


if __name__ == '__main__':
    main(False)
