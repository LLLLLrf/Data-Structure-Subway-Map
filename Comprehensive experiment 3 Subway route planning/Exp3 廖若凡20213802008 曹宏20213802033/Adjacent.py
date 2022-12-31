"""邻接点对象，用于存储站点相关数据，包括站点名称(name),站点出度(subgraph),站点所属路线(line)"""


class Station:
    def __init__(self, stationName):
        self.name = stationName
        self.subgraph = {}
        self.line = []
