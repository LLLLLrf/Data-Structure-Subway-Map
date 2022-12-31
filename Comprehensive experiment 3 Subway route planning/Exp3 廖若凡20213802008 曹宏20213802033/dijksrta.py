import pickle
import pandas
import os
from collections import defaultdict
import pickle
from geopy.distance import geodesic
INF=0x3f3f3f3f
    
def dijksrta(start,end):
    file=open('graph.pkl','rb')
    graph=pickle.load(file)
    book={}
    dis={}
    path={}
    for i in graph:
        book[i]=0
        path[i]=None
        if graph[start].get(i,None)!=None:
            dis[i]=graph[start][i]
            path[i]=start
        else:
            dis[i]=INF
    book[start]=1
    for i in range(len(graph)):
        minv=INF
        minn=None
        for i in dis:
            if book[i]==0 and dis[i]<minv:
                minv=dis[i]
                minn=i
        book[minn]=1
        for i in dis:
            if graph[minn].get(i,None)!=None and dis[i]>dis[minn]+graph[minn][i]:
                dis[i]=dis[minn]+graph[minn][i]
                path[i]=minn
    way=[]
    way.append(end)
    nowsta=end
    while nowsta!=start:
        if path[nowsta]!=None:
            way.append(path[nowsta])
            nowsta=path[nowsta]
    way.reverse()
    return way

def get_graph():
    print('正在创建pickle文件...')
    data=pandas.read_excel('./subway.xlsx')
    graph=defaultdict(dict)
    for i in range(data.shape[0]):
        site1=data.iloc[i]['site']
        if i<data.shape[0]-1:
            site2=data.iloc[i+1]['site']
            if site1==site2:
                longitude1,latitude1=data.iloc[i]['longitude'],data.iloc[i]['latitude']
                longitude2,latitude2=data.iloc[i+1]['longitude'],data.iloc[i+1]['latitude']
                name1=data.iloc[i]['name']
                name2=data.iloc[i+1]['name']
                distance=geodesic((float(longitude1),float(latitude1)), (float(longitude2),float(latitude2))).m
                graph[name1][name2]=distance
                graph[name2][name1]=distance
    output=open('graph.pkl','wb')
    pickle.dump(graph,output)

def main(site1,site2):
    if not os.path.exists('./subway.xlsx'):
        raise FileExistsError("Lack of information about Guangzhou Metro stations.")
    if not os.path.exists('./graph.pkl'):
        get_graph()
    path_result=dijksrta(site1,site2)
    print('路线如下：'+'-->'.join(path_result))
    return path_result

if __name__=='__main__':
    start=input("请输入起点站：")
    end=input("请输入终点站：")
    main(start,end)