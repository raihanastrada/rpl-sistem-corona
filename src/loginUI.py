import sys
import loginQueries as lq
import registerUI as rUI
import mainmenu
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

def clear(dialog):
    dialog.line_email.clear()
    dialog.line_password.clear()
    return

def login_clicked(dialog):
    email = dialog.line_email.text()
    password = dialog.line_password.text()
    if email == "" or password == "":
        dialog.lbl_notification.setText("Tolong isi email dan password dengan benar")
        return
    if not lq.isEmailExist(email):
        dialog.lbl_notification.setText("Email belum terdaftar, silahkan register")
        clear(dialog)
        return
    loginInfo = lq.getLoginInfo(email)
    databasePass = loginInfo[0]
    databaseRole = loginInfo[1]
    if password != databasePass:
        dialog.lbl_notification.setText("Password salah")
        clear(dialog)
        return
    clear(dialog)
    dialog.close()
    main_page = mainmenu.MainMenu(email)
    main_page.show()
    # Jika password benar, maka akan ke Main Menu
    return

def register_clicked(dialog):
    dialog.close()
    register_page = rUI.Register()
    register_page.exec_()
    return

def Login():
    dialog = QtWidgets.QDialog()
    loadUi('login.ui', dialog)
    dialog.setWindowTitle("Login Form")
    dialog.btn_login.clicked.connect(lambda: login_clicked(dialog))
    dialog.btn_register.clicked.connect(lambda: register_clicked(dialog))
    return dialog

def startLogin():
    app = QtWidgets.QApplication(sys.argv)
    dialog = Login()
    dialog.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    startLogin()
