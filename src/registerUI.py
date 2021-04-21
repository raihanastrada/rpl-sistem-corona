import sys
import loginQueries as lq
import loginUI as lUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

def login_clicked(dialog):
    dialog.close()
    login_page = lUI.Login()
    login_page.exec_()
    return

def register_clicked(dialog):
    nama = dialog.line_nama.text()
    email = dialog.line_email.text()
    password = dialog.line_password.text()
    upin = dialog.line_pin.text()
    number = dialog.line_number.text()
    if nama == "" or email == "" or password == "" or upin == "" or number == "":
        dialog.lbl_notification.setText("Tolong untuk mengisi seluruh bagian dengan benar")
        return
    if lq.isEmailExist(email):
        dialog.lbl_notification.setText("E-mail sudah terdaftar, silahkan login")
        return
    if len(upin) != 4 or upin.isdecimal() == False:
        dialog.lbl_notification.setText("PIN harus merupakan angka berjumlah 4")
        return
    if number.isdecimal() == False:
        dialog.lbl_notification.setText("Nomor telepon harus merupakan angka")
        return
    lq.addCustomerEntry(nama, email, password, number, upin)
    dialog.close()
    login_page = lUI.Login()
    login_page.exec_()
    return

def Register():
    dialog = QtWidgets.QDialog()
    loadUi('../screens/RegistrationScreen.ui', dialog)
    dialog.setWindowTitle("Register Form")
    dialog.btn_login.clicked.connect(lambda: login_clicked(dialog))
    dialog.btn_register.clicked.connect(lambda: register_clicked(dialog))
    return dialog

def startRegister():
    app = QtWidgets.QApplication(sys.argv)
    dialog = Register()
    dialog.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    startRegister()
