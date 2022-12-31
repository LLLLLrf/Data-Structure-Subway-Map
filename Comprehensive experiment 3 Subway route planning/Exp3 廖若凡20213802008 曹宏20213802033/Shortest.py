INF = 0x3f3f3f3f

'''
————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
以下为求最短路径使用的函数
'''

'''dijksrta算法求单源最短路'''


def dijksrta(start, end, graph):
    # 初始化标记字典、距离字典、路径字典
    book = {}
    dis = {}
    path = {}
    for i in graph:
        book[i] = 0
        path[i] = None
        if graph[start].subgraph.get(i, None) is not None:
            dis[i] = graph[start].subgraph[i]
            path[i] = start
        else:
            dis[i] = INF
    book[start] = 1

    # 当存在未标记站点时重复寻找距离最近的未标记站点,并更新距离字典
    while min(book.values()) == 0:
        # 初始化最小距离和最小距离节点名
        minv = INF
        minn = None
        # 寻找并标记最小距离站点
        for i in dis:
            if book[i] == 0 and dis[i] < minv:
                minv = dis[i]
                minn = i
        book[minn] = 1
        # 更新距离字典并标记路径
        for i in dis:
            if graph[minn].subgraph.get(i, None) is not None and dis[i] > dis[minn] + graph[minn].subgraph[i]:
                dis[i] = dis[minn] + graph[minn].subgraph[i]
                path[i] = minn
    # 根据路径字典得到全部最短路径并返回
    way = [end]
    nowsta = end
    while nowsta != start:
        if path[nowsta] is not None:
            way.append(path[nowsta])
            nowsta = path[nowsta]
    way.reverse()
    return way, dis[end]
