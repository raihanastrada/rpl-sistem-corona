from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
import sqlite3
import rsQueries

def rs_picked(widget):
    picked_rs = widget.rs_pick.currentText()
    email = "nolercustomer@gmail.com"
    rsQueries.addPemesananEntry(picked_rs, email)
    widget.label_5.setText(widget.label_5.text() + "completed.")
    return

def buatPemesananButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(1)
    all_rs = rsQueries.getAllRS()
    for i in range(len(all_rs)):
        widget.rs_pick.addItem(all_rs[i][1])
    widget.btn_rspick.clicked.connect(lambda: rs_picked(widget))
    return 

def lihatPemesananButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(2)
    email = "nolercustomer@gmail.com"
    email_pesanan = rsQueries.getOngoingPesananUser(email)
    if (not email_pesanan):
        widget.label_4.setText(widget.label_4.text() + " anda ditolak atau tidak tercatat")
    else:
        for i in range(len(email_pesanan)):
            rs_name = rsQueries.getRSName(email_pesanan[i][2])
            review_status = rsQueries.getOngoingPesananUser(email)
            if (review_status == None):
                widget.label_4.setText(widget.label_4.text() + " " + rs_name + " belum direview")
            else:
                widget.label_4.setText(widget.label_4.text() + " " + rs_name + " sudah direview")      
    return 

def mainButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(0)
    return

def bayarButton_clicked():
    print("bayar clicked but not implemented")
    return

def screenPesanRumahSakit():
    widget = QtWidgets.QWidget()
    loadUi('PesanRumahSakit.ui', widget)
    widget.setWindowTitle(" Pemesanan Rumah Sakit ")
    widget.btn_buat.clicked.connect(lambda: buatPemesananButton_clicked(widget))
    widget.btn_lihat.clicked.connect(lambda: lihatPemesananButton_clicked(widget))
    widget.btn_back1.clicked.connect(lambda: mainButton_clicked(widget))
    widget.btn_back2.clicked.connect(lambda: mainButton_clicked(widget))
    return widget

def main_test():
    app = QtWidgets.QApplication(sys.argv)
    widget = screenPesanRumahSakit()
    widget.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    main_test()
