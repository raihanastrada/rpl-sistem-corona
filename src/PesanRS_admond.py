from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
import sqlite3
import rsQueries

def reviewPemesananButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(1)
    widget.label_2.clear()
    not_reviewed = rsQueries.getAllPesananNotReviewed()
    for i in range(len(not_reviewed)):
        user_id = not_reviewed[i][1]
        rs_name = rsQueries.getRSName(not_reviewed[i][2])
        widget.label_2.setText(widget.label_2.text() + " user id " + str(user_id) + ", " + rs_name + '\n')
    return

def acceptButton_clicked(widget):
    return

def rejectButton_clicked(widget):
    return

def riwayatButton_clicked(widget):
    return

def backButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(0)
    return

def screenPesanRumahSakitAdmond():
    widget = QtWidgets.QWidget()
    loadUi('ScreenPesanRumahSakitAdmond.ui', widget)
    widget.setWindowTitle(" Pemesanan Rumah Sakit for Admondo")
    widget.btn_review.clicked.connect(lambda: reviewPemesananButton_clicked(widget))
    widget.btn_acc.clicked.connect(lambda: acceptButton_clicked(widget))
    widget.btn_reject.clicked.connect(lambda: rejectButton_clicked(widget))
    widget.btn_riwayat.clicked.connect(lambda: riwayatButton_clicked(widget))
    widget.btn_back1.clicked.connect(lambda: backButton_clicked(widget))
    return widget

def main_test():
    app = QtWidgets.QApplication(sys.argv)
    widget = screenPesanRumahSakitAdmond()
    widget.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    main_test()
