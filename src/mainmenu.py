import sys
import loginQueries as lq
import loginUI as lUI
import PesanRS as prs
import PesanRS_admond as prsA
import kasusHarian as kasus
import membership as mem
import suhuTubuhMenu as stm
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.uic import loadUi

import test # TEST

def account_clicked(window, email):
    text = "E-mail: " + email + "\n"
    text += "Name: " + lq.getName(email) + "\n"
    if lq.getMembershipStatus(email)[0] == False:
        memStatus = "Membership status: Not a member\n"
    else:
        memStatus = "Membership status: Member\n"
    memStatus += "Akun Customer\n"
    text += memStatus
    window.lbl_info.setText(text)
    window.lbl_info.setAlignment(QtCore.Qt.AlignCenter)
    window.stack_widget.setCurrentIndex(0)
    return

def suhu_clicked(window):
    window.stack_widget.setCurrentIndex(1)
    return

def harian_clicked(window):
    window.stack_widget.setCurrentIndex(2)
    return

def pesan_clicked(window):
    window.stack_widget.setCurrentIndex(3)
    return

def member_clicked(window):
    window.stack_widget.setCurrentIndex(4)
    return

def logout_clicked(window):
    window.close()
    login_page = lUI.Login()
    login_page.exec_()
    return

def MainMenu(email):
    window = QtWidgets.QMainWindow()
    try:
        loadUi('../screens/MainCustomerScreen.ui', window)
    except:
        loadUi('screens/MainCustomerScreen.ui', window)
    window.setWindowTitle("Sistem Tracking Corona Menu")
    window.btn_account.clicked.connect(lambda: account_clicked(window, email))
    window.btn_suhu.clicked.connect(lambda: suhu_clicked(window))
    window.btn_harian.clicked.connect(lambda: harian_clicked(window))
    window.btn_pesan.clicked.connect(lambda: pesan_clicked(window))
    window.btn_member.clicked.connect(lambda: member_clicked(window))
    window.btn_logout.clicked.connect(lambda: logout_clicked(window))
    text = "E-mail: " + email + "\n"
    text += "Name: " + lq.getName(email) + "\n"
    if lq.getMembershipStatus(email)[0] == False:
        memStatus = "Membership status: Not a member\n"
    else:
        memStatus = "Membership status: Member\n"
    memStatus += "Akun Customer\n"
    text += memStatus
    window.lbl_info.setText(text)
    window.lbl_info.setAlignment(QtCore.Qt.AlignCenter)
    # Menambahkan widget (harus berurutan)
    window.stack_widget.addWidget(stm.screenSuhu(lq.getUserID(email))) # Widget Suhu Tubuh
    window.stack_widget.addWidget(kasus.kasusHarian(False)) # Widget Kasus
    window.stack_widget.addWidget(prs.screenPesanRumahSakit(email)) # Widget Pemesanan Rumah Sakit
    window.stack_widget.addWidget(mem.membershipWindow(email)) # Widget Member
    return window

def startMainMenu(email):
    app = QtWidgets.QApplication(sys.argv)
    window = MainMenu(email)
    window.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    startMainMenu('nolercustomer@gmail.com')