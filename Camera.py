from CamShow import Ui_CamShow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
import cv2
import qimage2ndarray
import water_identification


class CamShow(QMainWindow, Ui_CamShow):

    def __del__(self):
        self.camera.release()  # 释放资源

    def __init__(self, parent=None):
        super(CamShow, self).__init__(parent)
        self.setupUi(self)
        self.PrepWidgets()  # 初始化各个控件
        self.PrepParameters()  # 定义并初始化程序运行过程中会用到的变量
        self.CallBackFunctions()  # 各个控件背后的功能函数的集合
        self.Timer = QTimer()
        self.Timer.timeout.connect(self.TimerOutFun)  # 定时器的调用

    # 初始化界面
    def PrepWidgets(self):
        self.StopBt.setEnabled(False)

    # 初始化变量
    def PrepParameters(self):
        self.Image_num = 0

    # 功能函数
    def CallBackFunctions(self):
        self.ShowBt.clicked.connect(self.StartCamera)
        self.StopBt.clicked.connect(self.StopCamera)

    # 连接按钮调整
    def StartCamera(self):
        url = 'rtsp://{0}:{1}@{2}//Streaming/Channels/1'
        # url = 'rtsp://admin:Cumt123456@192.168.1.64//Streaming/Channels/1'
        self.ShowBt.setEnabled(False)
        self.StopBt.setEnabled(True)
        self.Timer.start(1)
        ip = self.ipaddress.text()
        account = self.account.text()
        password = self.password.text()
        url = url.format(account, password, ip)
        try:
            self.camera = cv2.VideoCapture(url)
            self.MsgTE.clear()
            self.MsgTE.append('Oboard camera connected.')
            self.MsgTE.setPlainText()
        except Exception as e:
            self.MsgTE.clear()
            self.MsgTE.append(str(e))
        # self.timelb = time.perf_counter()

    # 停止按钮调整
    def StopCamera(self):
        if self.StopBt.text() == '暂停':
            self.StopBt.setText('继续')
            self.Timer.stop()
        elif self.StopBt.text() == '继续':
            self.StopBt.setText('暂停')
            self.Timer.start(1)

    def TimerOutFun(self):
        success, frame = self.camera.read()
        if success:
            self.Image = frame
            self.DispImg()
            water_identification
            self.MsgTE.setPlainText('图像获取成功，水位线数值为...')
        else:
            self.MsgTE.clear()
            self.MsgTE.setPlainText('图像获取失败...')
            self.StopBt.setEnabled(False)
            self.ShowBt.setEnabled(True)
            self.ShowBt.setText('重新连接')
            self.Reconnet()


    def Reconnet(self):
        success, frame = self.camera.read()
        if success:
            self.Image = frame
            self.DispImg()
            self.ShowBt.setEnabled(False)
            self.StopBt.setEnabled(True)
            self.MsgTE.setPlainText('图像获取成功，水位线数值为...')
        else:
            self.MsgTE.clear()
            self.MsgTE.setPlainText('图像获取失败...')
            self.StopBt.setEnabled(False)
            self.ShowBt.setEnabled(True)
            self.ShowBt.setText('重新连接')

    def DispImg(self):
        img = cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)
        qimg = qimage2ndarray.array2qimage(img)
        self.DispLb.setPixmap(QPixmap(qimg))
        self.DispLb.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = CamShow()
    ui.show()
    sys.exit(app.exec_())
