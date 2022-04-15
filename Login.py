import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from Camera import CamShow
from login_UI import Ui_login_UI

app = QApplication(sys.argv)
user = {'root': '88888888'}
user_name = ''
user_passwd = ''
child = CamShow()


class Login(Ui_login_UI, QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.CallBackFunctions()

    def CallBackFunctions(self):
        self.login.clicked.connect(self.Login)

    def show_emppasswd(self):
        QMessageBox.information(self, "错误", "用户名或密码不能为空", QMessageBox.Ok)

    def show_wrong(self):
        QMessageBox.information(self, "错误", "用户名或密码错误", QMessageBox.Ok)

    def show_noaccount(self):
        QMessageBox.information(self, "错误", "用户名不存在", QMessageBox.Ok)

    def Login(self):
        user_name = self.useraccount.text()
        user_passwd = self.userpassword.text()
        if user_passwd == '' or user_name == '':
            self.show_emppasswd()
        else:
            with open('user.txt') as f:
                user = eval(f.read())
            if user_name not in user:
                self.show_noaccount()
            else:
                if user_passwd != user[user_name]:
                    self.show_wrong()
                    self.userpassword.clear()
                else:
                    child.show()
                    window.close()


window = Login()
window.show()
sys.exit(app.exec_())
