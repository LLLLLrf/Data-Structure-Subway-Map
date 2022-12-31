import tkinter as tk
import webbrowser
from ttkbootstrap import Style

'''
————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
以下为交互界面使用的函数
'''

'''
用于生成交互界面方便用户查找
'''


def interactiveInterface(graph):
    global start, end, mode
    start, end, mode = '', '', 2
    style = Style(theme='yeti')
    # 界面样式主题：['vista', 'classic', 'cyborg', 'journal', 'darkly', 'flatly', 'clam', 'alt', 'solar',√ 'minty',
    # 'litera', 'united', 'xpnative', 'pulse', 'cosmo', √'lumen', 'yeti', 'superhero', 'winnative', 'sandstone',
    # 'default']
    window = style.master
    window.title('广州地铁线路查询系统')
    window.geometry('500x260+400+300')

    la1 = tk.Label(window, text='广州地铁线路查询系统', padx=10, pady=18, font=('黑体', 13))
    la1.pack()
    entry1 = tk.Entry(window, width=20)
    entry1.pack()
    entry2 = tk.Entry(window, width=20)
    entry2.pack()
    # 用tk的StringVar类来辅助控件动态改变值
    str1 = tk.StringVar()
    str2 = tk.StringVar()
    # 定义文字标签控件
    warn = tk.Label(window, textvariable=str1, fg='red', font=('宋体', 10))
    warn2 = tk.Label(window, textvariable=str2, fg='red', font=('宋体', 10))
    tk.Label(window, text='起始站').place(x=130, y=55, anchor='nw')
    tk.Label(window, text='终点站').place(x=130, y=80, anchor='nw')

    def getStationName(mod):
        global start, end, mode
        start = entry1.get()  # 调用get()方法，将Entry中的内容获取出来
        end = entry2.get()
        mode = mod
        right_input = True
        # 判断输入站名是否存在
        if graph.get(start, None) is None:
            warn.place(x=330, y=55, anchor='nw')
            # 不存在则将动态的StringVar修改为报错
            str1.set("站点不存在！")
            right_input = False
        else:
            # 存在则隐藏报错
            str1.set("")
        if graph.get(end, None) is None:
            warn2.place(x=330, y=80, anchor='nw')
            str2.set("站点不存在！")
            right_input = False
        else:
            str2.set("")
        # 只要有一个不存在的站就不退出界面
        if not right_input:
            return
        # 否则退出界面
        window.destroy()

    # 不同按钮触发不同模式
    def setMode0():
        getStationName(0)

    def setMode1():
        getStationName(1)

    tk.Button(window, text='最短路径', command=setMode0).place(x=190, y=110, anchor='nw')
    tk.Button(window, text='最少换乘', command=setMode1).place(x=250, y=110, anchor='nw')
    tk.Button(window, text='查看广州地铁路线图', command=openWeb).place(x=190, y=145, anchor='nw')

    window.mainloop()
    return start, end, mode


def openWeb():
    # 通过webbrowser打开广州地铁路线图
    webbrowser.open_new_tab('Guangzhou_railway.html')
