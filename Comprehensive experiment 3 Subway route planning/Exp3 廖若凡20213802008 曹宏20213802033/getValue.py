# -*- coding:utf-8 -*-
import os
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView


class BridgeClass(QObject):
    """
       一个槽函数供js调用(内部最终将js的调用转化为了信号),
       一个信号供js绑定,
       这个一个交互对象最基本的组成部分.
    """

    # pyqtSlot，网络上大多将其翻译为槽。作用是接收网页发起的信号
    @pyqtSlot()
    def changeJsValueByPy(self):
        web_view.page().runJavaScript('defaulitValue="value from python"')

    # 注意pyqtSlot用于把该函数暴露给js可以调用
    @pyqtSlot()
    def callPy2JsByJs1(self):
        print('中间代理')
        self.pyCalljs('py呼叫js，收到请回答')

    def pyCalljs(self, msg):
        web_view.page().runJavaScript("pyCalljs('%s')" % msg, self.js_callback)
        print(msg)  # 查看参数

    # 回调函数，接收js返回的值
    def js_callback(self, result):
        QMessageBox.information(None, "提示", "来自js回复：{}".format(result))
        print(result)


    # 注意pyqtSlot用于把该函数暴露给js可以调用 result=str返回的值string
    @pyqtSlot(str, result=str)
    def jsCallpy(self, text):
        QMessageBox.information(None, "提示", "来自js消息：{}".format(text))
        return 'js,py收到消息'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 新增一个浏览器引擎
    web_view = QWebEngineView()
    # 增加一个通信中需要用到的频道
    myChannel = QWebChannel()
    # 用于通信的对象
    bridgeClass = BridgeClass()
    # 注册，testObject是自己起的名字
    myChannel.registerObject('Bridge', bridgeClass)
    # 在浏览器中设置该频道
    web_view.page().setWebChannel(myChannel)

    # 获取当前文件夹位置
    path_url = os.path.abspath('.')
    url_string = 'file://' + path_url + '/web.html'
    web_view.load(QUrl(url_string))
    web_view.show()
    sys.exit(app.exec_())