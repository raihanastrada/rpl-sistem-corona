from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
import sqlite3
import rsQueries

def reviewPemesananButton_clicked(widget):
    widget.stackedWidget.setCurrentIndex(1)
    not_reviewed = rsQueries.getAllPesananNotReviewed()
    if (not not_reviewed):
        widget.stackedWidget.setCurrentIndex(0)
    else:
        for i in range(len(not_reviewed)):
            order_id = not_reviewed[i][0]
            user_id = not_reviewed[i][1]
            rs_name = rsQueries.getRSName(not_reviewed[i][2])
            box_string = "order id " + str(order_id) + ", " + \
                "user id " + str(user_id) + ", " + rs_name + '\n'
            widget.list_pesan.addItem(box_string)
    return

def acceptButton_clicked(widget):
    widget.label_2.clear()
    box_string = widget.list_pesan.currentText()
    box_string = box_string.split(" ")
    order_id = int(box_string[2][:-1])
    review_status = rsQueries.setPesananReviewed(order_id)
    if (review_status):
        widget.label_2.setText(widget.label_2.text() + "review accepted.")
    else:
        widget.label_2.setText(widget.label_2.text() + "review's not processed.")
    return

def rejectButton_clicked(widget):
    widget.label_2.clear()
    box_string = widget.list_pesan.currentText()
    box_string = box_string.split(" ")
    order_id = int(box_string[2][:-1])
    review_status = rsQueries.deletePemesananEntry(order_id)
    if (review_status):
        widget.label_2.setText(widget.label_2.text() + "review rejected.")
    else:
        widget.label_2.setText(widget.label_2.text() + "review's not processed.")
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
