import sys
import loginQueries as lq
import loginUI as lUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

def account_clicked(window):
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
    loadUi('mainDialog.ui', window)
    window.setWindowTitle("Sistem Tracking Corona Menu")
    window.btn_account.clicked.connect(lambda: account_clicked(window))
    window.btn_suhu.clicked.connect(lambda: suhu_clicked(window))
    window.btn_harian.clicked.connect(lambda: harian_clicked(window))
    window.btn_pesan.clicked.connect(lambda: pesan_clicked(window))
    window.btn_member.clicked.connect(lambda: member_clicked(window))
    window.btn_logout.clicked.connect(lambda: logout_clicked(window))
    text = "E-mail: " + email + "\n"
    text += "Name: " + lq.getName(email) + "\n"
    if lq.getMembershipStatus(email) == False:
        memStatus = "Membership status: Not a member\n"
    else:
        memStatus = "Membership status: Member\n"
    text += memStatus
    window.lbl_info.setText(text)
    # Menambahkan widget (harus berurutan)
    # window.stack_widget.addWidget("""WidgetSuhu""")
    # window.stack_widget.addWidget("""WidgetHarian""")
    # window.stack_widget.addWidget("""WidgetPesan""")
    # window.stack_widget.addWidget("""WidgetMember""")
    return window

def startMainMenu(email):
    app = QtWidgets.QApplication(sys.argv)
    window = MainMenu(email)
    window.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    startMainMenu('customernoler@gmail.com')