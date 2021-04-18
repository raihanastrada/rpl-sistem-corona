import sys
import loginQueries as lq
import loginUI as lUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

def suhu_clicked():
    print("Suhu clicked")
    return

def harian_clicked():
    print("Harian clicked")
    return

def member_clicked():
    print("Member clicked")
    return

def pesan_clicked():
    print("Pesan clicked")
    return

def logout_clicked(dialog):
    dialog.close()
    login_page = lUI.LoginProcedural()
    login_page.exec_()
    return

def MainMenuProcedural(email):
    dialog = QtWidgets.QDialog()
    loadUi('mainDialog.ui', dialog)
    dialog.setWindowTitle("Sistem Tracking Corona Menu")
    dialog.btn_suhu.clicked.connect(suhu_clicked)
    dialog.btn_harian.clicked.connect(harian_clicked)
    dialog.btn_pesan.clicked.connect(pesan_clicked)
    dialog.btn_member.clicked.connect(member_clicked)
    dialog.btn_logout.clicked.connect(lambda: logout_clicked(dialog))
    text = "E-mail: " + email + "\n"
    text += "Name: " + lq.getName(email) + "\n"
    if lq.getMembershipStatus(email) == False:
        memStatus = "Membership status: Not a member\n"
    else:
        memStatus = "Membership status: Member\n"
    text += memStatus
    dialog.lbl_info.setText(text)
    return dialog

def startMainMenuProcedural(email):
    app = QtWidgets.QApplication(sys.argv)
    dialog = MainMenuProcedural(email)
    sys.exit(dialog.exec_())
    dialog.show()

if __name__ == "__main__":
    startMainMenuProcedural('customernoler@gmail.com')