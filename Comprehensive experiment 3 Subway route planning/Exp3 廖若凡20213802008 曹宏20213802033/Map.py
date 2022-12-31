import requests
import time
import numpy as np
from geopy.distance import geodesic
import webbrowser
import math
import plotly.offline as py
import plotly.graph_objs as go
import random

INF = 0x3f3f3f3f

'''
————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
以下为生成路线图使用的函数
'''

'''用于定义生成html文件相关的全局变量,爬取广州地铁数据'''


def pre_plot():
    # 定义json中关键字对应的python中的值,爬取广州地铁数据
    global colors, data, layout, station_info_json, false, true, null, lineDic
    false, true, null = False, True, None
    mapbox_access_token = (
        'pk.eyJ1IjoibHVrYXNtYXJ0aW5lbGxpIiwiYSI6ImNpem85dmhwazAyajIyd284dGxhN2VxYnYifQ.HQCmyhEXZUTz3S98FMrVAQ'
    )
    station_info = requests.get('http://map.baidu.com/?qt=bsi&c=%s&t=%s' % (
        257,
        int(time.time() * 1000)
    )
                                )
    station_info_json = eval(station_info.content)  # 将json字符串转为python对象
    layout = go.Layout(
        autosize=True,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=23.12864583,  # 广州市纬度
                lon=113.2648325  # 广州市经度
            ),
            pitch=0,
            zoom=10
        ),
    )
    colors = ('blue', 'green', 'yellow', 'purple', 'orange', 'red', 'violet',
              'navy', 'crimson', 'cyan', 'magenta', 'maroon', 'peru')
    data = []  # 绘制数据
    lineDic = {}


'''用于获取子路径站点的相关数据,添加到html文件中并打开html文件'''


def plotGraph(site1, site2, path, line, distance, ifTest):
    # 根据起点和终点对路径进行切片,得到子路径
    if site2 is None:
        stationList = path[site1:]
    else:
        stationList = path[site1:site2]
    # 针对爬取的地铁线数据与原图数据不一致的情况进行特殊处理
    if 'APM' in line:
        line = 'APM线' + line[line.index('('):]
    # 根据字符匹配获得子路径所属地铁线的uid
    uid, railway = '', {}
    for railwayLine in station_info_json['content']:
        if line[2:] in railwayLine['line_name'] and not ('佛山' in railwayLine['line_name']):
            uid = railwayLine['line_uid']
            railway = railwayLine
            break
            # 通过uid爬取地铁线数据
    railway_json = requests.get(
        'https://map.baidu.com/?qt=bsl&tps=&newmap=1&uid=%s&c=%s' % (uid, 257)
    )
    railway_json = eval(railway_json.content)  # 将json字符串转为python对象
    # 取出地铁线的线段坐标
    trace_mercator = np.array(
        railway_json['content'][0]['geo'].split('|')[2][: -1].split(','),
        dtype=float
    ).reshape((-1, 2))
    # 将得到的线段的墨卡托投影坐标转换为生成html所需编码的线段坐标
    trace_coordinates = gcj02_to_wgs84(bd09_to_gcj02((mercator_to_bd09(trace_mercator))))
    # 取出站点坐标
    plots = []
    plots_name = []
    for plotSta in railway['stops']:
        if plotSta['name'] in stationList:
            plots.append([plotSta['x'], plotSta['y']])
            plots_name.append(plotSta['name'])
    plot_mercator = np.array(plots)
    # 将加密的站点坐标转换为生成html所需编码的站点坐标
    plot_coordinates = gcj02_to_wgs84(bd09_to_gcj02((mercator_to_bd09(plot_mercator))))  # 站台经纬度
    # 初始化最小距离和最小距离路线名称
    min_DTSv, min_DTEv = INF, INF
    min_DTSn, min_DTEn = '', ''
    # 遍历线路坐标,分别找出离子路径起点和终点最近的线段
    for lineNumber in range(len(trace_coordinates)):
        distanceToStart = geodesic((float(trace_coordinates[lineNumber][1]), float(trace_coordinates[lineNumber][0])),
                                   (float(plot_coordinates[0][1]), float(plot_coordinates[0][0]))).m
        distanceToEnd = geodesic((float(trace_coordinates[lineNumber][1]), float(trace_coordinates[lineNumber][0])),
                                 (float(plot_coordinates[-1][1]), float(plot_coordinates[-1][0]))).m
        if distanceToStart < min_DTSv:
            min_DTSv = distanceToStart
            min_DTSn = lineNumber
        if distanceToEnd < min_DTEv:
            min_DTEv = distanceToEnd
            min_DTEn = lineNumber
    # 采用切片以保留子路径起点到终点之间的所有线段
    trace_coordinates = trace_coordinates[min_DTSn:min_DTEn + 1]
    # 设置线路颜色
    color = railway_json['content'][0]['lineColor']
    if color == '':
        color = random.choice(colors)
    # 对传入线路关键字进行重新处理,以得到用于图例展示的线路名称
    update = []
    for i in railway['line_name']:
        if i == '(':
            break
        update.append(i)
    lineName = ''.join(update) + '(%s-%s)' % (stationList[0], stationList[-1])
    lineDic[path[site1]] = ''.join(update)
    # 将地铁路线和站点数据加入data中
    data.extend([
        # 地铁路线
        go.Scattermapbox(
            lon=trace_coordinates[:, 0],  # 路线点经度
            lat=trace_coordinates[:, 1],  # 路线点纬度
            mode='lines',
            # 设置路线的参数
            line=go.scattermapbox.Line(
                width=2,
                color=color
            ),
            name=lineName,  # 线路名称，显示在图例（legend）上
            legendgroup=lineName
        ),
        # 地铁站台
        go.Scattermapbox(
            lon=plot_coordinates[:, 0],  # 站台经度
            lat=plot_coordinates[:, 1],  # 站台纬度
            mode='markers',
            text=plots_name,
            # 设置标记点的参数
            marker=go.scattermapbox.Marker(
                size=10,
                color=color
            ),
            name=lineName,  # 线路名称，显示在图例（legend）及鼠标悬浮在标记点时的路线名上
            legendgroup=lineName,  # 设置与路线同组，当隐藏该路线时隐藏标记点
            showlegend=False  # 不显示图例（legend)
        )
    ])
    fig = dict(data=data, layout=layout)
    # 若当前子路径终点为路径终点,则生成html文件并打开
    if stationList[-1] == path[-1]:
        # 生成html文件
        if distance[0] > 19:
            modeStr = '最短路径'
        else:
            modeStr = '最少换乘次数路径'
        fileName = 'Guangzhou_railway_recommend_%s-%s(%s).html' % (path[0], path[-1], modeStr)
        py.plot(fig, filename=fileName, auto_open=False)
        # 向html文件添加推荐路径文字信息
        for j in lineDic:
            if j == path[0]:
                path[path.index(j)] = '(' + lineDic[j] + ')' + path[path.index(j)]
                continue
            path[path.index(j)] = path[path.index(j)] + '(转' + lineDic[j] + ')'
        if distance[0] > 19:
            # path[-1]=path[-1]+' '+'路径长度：{0}km'.format(int(distance[0])/1000)
            path.append('路径长度：{0}km'.format(int(distance[0]) / 1000))
        else:
            # path[-1]=path[-1]+' '+'换乘次数：{0}次，路径长度：{1}km'.format(distance[0],int(distance[1])/1000)
            path.append('换乘次数：{0}次   路径长度：{1}km'.format(distance[0], int(distance[1]) / 1000))
        htmlChange(path, fileName)
        # 判断是否为测试模式,是则输出最短路径/最少换乘次数路径,否则打开html文件
        if not ifTest:
            webbrowser.open_new_tab(fileName)
        else:
            if distance[0] > 19:
                print('最短路径为：' + '-->'.join(path[:-1]) + ' ' + path[-1])
            else:
                print('最少换乘次数路径为：' + '-->'.join(path[:-1]) + ' ' + path[-1])


'''
用于生成html文件的前置工作,生成路线图的html文件
根据路径判断换线站点,以此得到子路径，
然后将子路径传入plotGraph()函数,向html文件中添加子路径站点的相关数据
'''


def plot(path, graph, distance, ifTest):
    # 生成html文件的前置工作
    pre_plot()
    # 初始化子路径索引以及地铁线判断列表
    plotstart = 0
    pathLine = []
    # 遍历路径以得到子路径
    for i in range(len(path)):
        # 判断是否为路径最后一个站点,是则添加最后一个子路径相关数据
        line = ''
        if i == len(path) - 1:
            for j in graph[path[plotstart]].line:
                if j in graph[path[i]].line:
                    line = j
            plotGraph(plotstart, None, path, line + '(' + get_linestart(line), distance, ifTest)
            continue
        # 将当前站点所属线路添加至地铁线判断列表
        for j in graph[path[i]].line:
            pathLine.append(j)
        # 判断当前站点是否属于可换乘站点,若是则可能为子路径终点
        if len(graph[path[i]].line) > 1 and i != len(path) - 1:
            # 统计地铁线判断列表中元素出现次数,出现次数最高的为子路径所属线路
            line1 = ''
            pathLineSet = set(pathLine)
            maxline = 0
            for j in pathLineSet:
                if pathLine.count(j) > maxline:
                    line1 = j
                    maxline = pathLine.count(j)
            # 判断是否属于可换乘站点但不是当前子路径终点的情况,是则跳过本次循环,否则向html文件中添加子路径站点的相关数据
            if line1 in graph[path[i + 1]].line or maxline == 1:
                continue
            else:
                plotGraph(plotstart, i + 1, path, line1 + '(' + get_linestart(line1), distance, ifTest)
                plotstart = i
                pathLine = []
                for j in graph[path[plotstart]].line:
                    pathLine.append(j)


'''用于返回当前地铁线头/尾站点的其中一个,用于与爬取地铁线数据进行匹配'''


def get_linestart(lineName):
    linestart = {'广州地铁1号线': '广州东站', '广州地铁2号线': '广州南站', '广州地铁3号线': '番禺广场',
                 '广州地铁3号线北延段': '机场北', '广州地铁4号线': '南沙客运港', '广州地铁5号线': '滘口',
                 '广州地铁6号线': '浔峰岗', '广州地铁7号线': '美的大道', '广州地铁8号线': '万胜围',
                 '广州地铁9号线': '飞鹅岭', '广州地铁13号线': '鱼珠', '广州地铁14号线': '嘉禾望岗',
                 '广州地铁14号线支线(知识城线)': '新和', '广州地铁18号线': '冼村', '广州地铁21号线': '员村',
                 '广州地铁22号线': '番禺广场', '广州地铁APM线': '林和西', '广州广佛线': '新城东'}
    return linestart[lineName]


'''用于向已生成的路线图添加推荐路线的文字信息'''


def htmlChange(res, fileName):
    # 读取前面生成的推荐路径html文件
    file = open(fileName, "r", encoding='utf-8')
    content = file.read()
    # 将列表合并为字符串
    route = '➜'.join(res[:-1])
    # 添加网页css样式
    styles = ['border-radius:12px;',
              'padding:6px 10px;',
              'margin:8px 10px;',
              'background-color:#84AF9B;',
              'font-weight:500;',
              'font-family:幼圆;',
              'font-size:1.3em;',
              'color:#fff;',
              ]
    css = "style='{0}'".format(''.join(styles))
    # 在html中插入如下html标签
    content_add = '<div {0}>推荐路线：{1}</div><pre><div {0}">{2}</div></pre>'.format(css, route, res[-1])
    # 插在<body>标签后
    pos = content.find("<body>") + 18
    # css全局样式设置
    body_css = 'style="height:92vh;"'
    if pos != -1:
        content = content[:pos - 3] + ' ' + body_css + content[pos - 3:pos] + content_add + content[pos:]
        file = open(fileName, "w", encoding='utf-8')
        file.write(content)
        file.close()


'''初步转换GCJ-02编码的精度'''


def _transformlat(coordinates):
    lng = coordinates[:, 0] - 105
    lat = coordinates[:, 1] - 35
    ret = -100 + 2 * lng + 3 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * np.sqrt(np.fabs(lng))
    ret += (20 * np.sin(6 * lng * math.pi) + 20 *
            np.sin(2 * lng * math.pi)) * 2 / 3
    ret += (20 * np.sin(lat * math.pi) + 40 *
            np.sin(lat / 3 * math.pi)) * 2 / 3
    ret += (160 * np.sin(lat / 12 * math.pi) + 320 *
            np.sin(lat * math.pi / 30.0)) * 2 / 3
    return ret


'''初步转换GCJ-02编码的纬度'''


def _transformlng(coordinates):
    lng = coordinates[:, 0] - 105
    lat = coordinates[:, 1] - 35
    ret = 300 + lng + 2 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * np.sqrt(np.fabs(lng))
    ret += (20 * np.sin(6 * lng * math.pi) + 20 *
            np.sin(2 * lng * math.pi)) * 2 / 3
    ret += (20 * np.sin(lng * math.pi) + 40 *
            np.sin(lng / 3 * math.pi)) * 2 / 3
    ret += (150 * np.sin(lng / 12 * math.pi) + 300 *
            np.sin(lng / 30 * math.pi)) * 2 / 3
    return ret


'''GCJ-02坐标转WGS-84坐标'''


def gcj02_to_wgs84(coordinates):
    ee = 0.006693421622965943  # 偏心率平方
    a = 6378245  # 长半轴
    lng = coordinates[:, 0]
    lat = coordinates[:, 1]
    is_in_china = (lng > 73.66) & (lng < 135.05) & (lat > 3.86) & (lat < 53.55)
    _transform = coordinates[is_in_china]  # 只对国内的坐标做偏移
    dlat = _transformlat(_transform)
    dlng = _transformlng(_transform)
    radlat = _transform[:, 1] / 180 * math.pi
    magic = np.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = np.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * np.cos(radlat) * math.pi)
    mglat = _transform[:, 1] + dlat
    mglng = _transform[:, 0] + dlng
    coordinates[is_in_china] = np.array([
        _transform[:, 0] * 2 - mglng, _transform[:, 1] * 2 - mglat
    ]).T
    return coordinates


'''BD-09坐标转GCJ-02坐标'''


def bd09_to_gcj02(coordinates):
    x_pi = math.pi * 3000 / 180
    x = coordinates[:, 0] - 0.0065
    y = coordinates[:, 1] - 0.006
    z = np.sqrt(x * x + y * y) - 0.00002 * np.sin(y * x_pi)
    theta = np.arctan2(y, x) - 0.000003 * np.cos(x * x_pi)
    lng = z * np.cos(theta)
    lat = z * np.sin(theta)
    coordinates = np.array([lng, lat]).T
    return coordinates


'''BD-09MC坐标转BD-09坐标'''


def mercator_to_bd09(mercator):
    MCBAND = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
    MC2LL = [[1.410526172116255e-08, 8.98305509648872e-06, -1.9939833816331,
              200.9824383106796, -187.2403703815547, 91.6087516669843,
              -23.38765649603339, 2.57121317296198, -0.03801003308653,
              17337981.2],
             [-7.435856389565537e-09, 8.983055097726239e-06, -0.78625201886289,
              96.32687599759846, -1.85204757529826, -59.36935905485877,
              47.40033549296737, -16.50741931063887, 2.28786674699375,
              10260144.86],
             [-3.030883460898826e-08, 8.98305509983578e-06, 0.30071316287616,
              59.74293618442277, 7.357984074871, -25.38371002664745,
              13.45380521110908, -3.29883767235584, 0.32710905363475,
              6856817.37],
             [-1.981981304930552e-08, 8.983055099779535e-06, 0.03278182852591,
              40.31678527705744, 0.65659298677277, -4.44255534477492,
              0.85341911805263, 0.12923347998204, -0.04625736007561,
              4482777.06],
             [3.09191371068437e-09, 8.983055096812155e-06, 6.995724062e-05,
              23.10934304144901, -0.00023663490511, -0.6321817810242,
              -0.00663494467273, 0.03430082397953, -0.00466043876332,
              2555164.4],
             [2.890871144776878e-09, 8.983055095805407e-06, -3.068298e-08,
              7.47137025468032, -3.53937994e-06, -0.02145144861037,
              -1.234426596e-05, 0.00010322952773, -3.23890364e-06,
              826088.5]]
    x = np.abs(mercator[:, 0])
    y = np.abs(mercator[:, 1])
    coef = np.array([
        MC2LL[index] for index in
        (np.tile(y.reshape((-1, 1)), (1, 6)) < MCBAND).sum(axis=1)
    ])
    return converter(x, y, coef)


'''将BD-09MC坐标进行转换'''


def converter(x, y, coef):
    x_temp = coef[:, 0] + coef[:, 1] * np.abs(x)
    x_n = np.abs(y) / coef[:, 9]
    y_temp = coef[:, 2] + coef[:, 3] * x_n + coef[:, 4] * x_n ** 2 + \
             coef[:, 5] * x_n ** 3 + coef[:, 6] * x_n ** 4 + coef[:, 7] * x_n ** 5 + \
             coef[:, 8] * x_n ** 6
    x[x < 0] = -1
    x[x >= 0] = 1
    y[y < 0] = -1
    y[y >= 0] = 1
    x_temp *= x
    y_temp *= y
    coordinates = np.array([x_temp, y_temp]).T
    return coordinates
