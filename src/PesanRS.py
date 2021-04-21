from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
import sqlite3
import rsQueries

def rs_picked(widget,email):
    widget.label_5.clear()
    picked_rs = widget.rs_pick.currentText()
    if (rsQueries.addPemesananEntry(picked_rs, email)):
        widget.label_5.setText(widget.label_5.text() + "Pemesanan completed.")
    else:
        widget.label_5.setText(widget.label_5.text() + "Anda tidak bisa memesan lagi.")
    return

def buatPemesananButton_clicked(widget,email):
    widget.stackedWidget.setCurrentIndex(1)
    all_rs = rsQueries.getAllRS()
    for i in range(len(all_rs)):
        widget.rs_pick.addItem(all_rs[i][1])
    widget.btn_rspick.clicked.connect(lambda: rs_picked(widget,email))
    return 

def lihatPemesananButton_clicked(widget,email):
    widget.label_4.clear()
    widget.stackedWidget.setCurrentIndex(2)
    email_pesanan = rsQueries.getReviewedPesananUser(email)
    if (not email_pesanan):
        widget.label_4.setText("Status pemesanan anda ditolak, belum diterima atau tidak tercatat")
    else:
        for i in range(len(email_pesanan)):
            rs_name = rsQueries.getRSName(email_pesanan[i][2])
            if (rsQueries.getOngoingPesananUser(email)):
                widget.label_4.setText("Status pemesanan anda di " + rs_name + " belum direview")
            else:
                widget.label_4.setText("Status pemesanan anda di " + rs_name + " sudah direview")      
    return 

def mainButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(0)
    return

def bayarButton_clicked(email):
    if (not rsQueries.getOngoingPesananUser(email)):
        print("bayar clicked but not implemented")
    else:
        print("mohon tunggu status review")
    return

def screenPesanRumahSakit(email):
    widget = QtWidgets.QWidget()
    try:
        loadUi('../screens/PesanRumahSakitScreen.ui', widget)
    except:
        loadUi('screens/PesanRumahSakitScreen.ui', widget)
    widget.setWindowTitle(" Pemesanan Rumah Sakit ")
    widget.btn_buat.clicked.connect(lambda: buatPemesananButton_clicked(widget,email))
    widget.btn_lihat.clicked.connect(lambda: lihatPemesananButton_clicked(widget,email))
    widget.btn_back1.clicked.connect(lambda: mainButton_clicked(widget))
    widget.btn_back2.clicked.connect(lambda: mainButton_clicked(widget))
    widget.btn_bayar.clicked.connect(lambda: bayarButton_clicked(email))
    return widget

def main_test():
    app = QtWidgets.QApplication(sys.argv)
    email = "nolercustomer@gmail.com"
    widget = screenPesanRumahSakit(email)
    widget.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    main_test()
