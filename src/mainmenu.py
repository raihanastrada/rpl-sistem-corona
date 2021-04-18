import sys
import loginQueries as lq
import loginUI as lUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

class MainMenu(QtWidgets.QDialog):
    def __init__(self, email):
        super().__init__()
        loadUi('mainDialog.ui', self)
        self.setWindowTitle("Sistem Tracking Corona Menu")
        self.btn_suhu.clicked.connect(self.suhu_clicked)
        self.btn_harian.clicked.connect(self.harian_clicked)
        self.btn_pesan.clicked.connect(self.pesan_clicked)
        self.btn_member.clicked.connect(self.member_clicked)
        self.btn_logout.clicked.connect(self.logout_clicked)
        text = "E-mail: " + email + "\n"
        text += "Name: " + lq.getName(email) + "\n"
        if lq.getMembershipStatus(email) == False:
            memStatus = "Membership status: Not a member\n"
        else:
            memStatus = "Membership status: Member\n"
        text += memStatus
        self.lbl_info.setText(text)

    def suhu_clicked(self):
        print("Suhu clicked")
        return

    def harian_clicked(self):
        print("Harian clicked")
        return

    def pesan_clicked(self):
        print("Pesan clicked")
        return

    def member_clicked(self):
        print("Member clicked")
        return

    def logout_clicked(self):
        self.close()
        login_page = lUI.Login()
        login_page.exec_()
        return

def startMainMenu(email):
    app = QtWidgets.QApplication(sys.argv)
    menu = MainMenu(email)
    menu.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    startMainMenu("customernoler@gmail.com")