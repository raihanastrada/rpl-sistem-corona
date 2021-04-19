from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
import sqlite3
#import rsQueries

def buatPemesananButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(1)
    return 

def lihatPemesananButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(2)
    return 

def bayarButton_clicked():
    print("bayar clicked")
    return

def mainButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(0)
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
