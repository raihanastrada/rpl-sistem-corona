import sys
import loginQueries as lq
import loginUI as lUI
import kasusHarian as kH
import PesanRS_admond as prsA
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

def account_clicked(window):
    window.stack_widget.setCurrentIndex(0)
    return

def harian_clicked(window):
    window.stack_widget.setCurrentIndex(1)
    return

def pesan_clicked(window):
    window.stack_widget.setCurrentIndex(2)
    return

def logout_clicked(window):
    window.close()
    login_page = lUI.Login()
    login_page.exec_()
    return

def MainMenuAdmin(email):
    window = QtWidgets.QMainWindow()
    loadUi('mainDialogAdmin.ui', window)
    window.setWindowTitle("Sistem Tracking Corona Menu - Admin")
    window.btn_account.clicked.connect(lambda: account_clicked(window))
    window.btn_harian.clicked.connect(lambda: harian_clicked(window))
    window.btn_pesan.clicked.connect(lambda: pesan_clicked(window))
    window.btn_logout.clicked.connect(lambda: logout_clicked(window))
    text = "E-mail: " + email + "\n"
    text += "Name: " + lq.getName(email) + "\n"
    text += "Akun Admin\n"
    window.lbl_info.setText(text)
    window.lbl_info.setAlignment(QtCore.Qt.AlignCenter)
    # Menambahkan widget (harus berurutan)
    window.stack_widget.addWidget(kH.kasusHarian(True)) # Widget harian admin
    window.stack_widget.addWidget(prsA.screenPesanRumahSakitAdmond()) # Widget pesanan admin
    return window

def startMainMenuAdmin(email):
    app = QtWidgets.QApplication(sys.argv)
    window = MainMenuAdmin(email)
    window.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    startMainMenuAdmin('adminnoler@gmail.com')