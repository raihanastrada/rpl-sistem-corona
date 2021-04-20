from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import suhuQueries as sQ

def submitSuhu_clicked(dialog):
    dialog.message.setText("")

    try:
        suhu = float(dialog.inputSuhuLineEdit.text())
    except:
        dialog.message.setText("Suhu tidak valid")
        return

    if (not sQ.addSuhuEntry(int(dialog.userid.text()), dialog.inputTanggalDateEdit.date(), suhu)):
        dialog.message.setText("Suhu pada tanggal tersebut sudah diisi")
    else:
        dialog.inputSuhuLineEdit.setText("")
    return

def lihatRiwayat_clicked(dialog):
    dialog.message.setText("")
    result = sQ.getRiwayatSuhuTubuh(int(dialog.userid.text()), dialog.dariTanggalDateEdit.date(), dialog.sampaiTanggalDateEdit.date())
    # if (not result):
    #     dialog.message.setText("Error getting temperature history")
    # else:
    dialog.tableWidget.setRowCount(len(result))
    for i in range(len(result)):
        dialog.tableWidget.setItem(i, 0, QTableWidgetItem(result[i][0]))
        dialog.tableWidget.setItem(i, 1, QTableWidgetItem(str(result[i][1])))
        dialog.tableWidget.setItem(i, 2, QTableWidgetItem(sQ.evaluasiSuhu(result[i][1])))
    return

def screenSuhu(user_id):
    dialog = QtWidgets.QDialog()
    loadUi('suhuTubuhMenu.ui', dialog)

    dialog.setWindowTitle("Suhu Tubuh")
    dialog.userid.setText(str(user_id))
    dialog.inputSuhuLineEdit.setValidator(QtGui.QDoubleValidator())

    dialog.submitSuhu.clicked.connect(lambda: submitSuhu_clicked(dialog))
    dialog.lihatRiwayat.clicked.connect(lambda: lihatRiwayat_clicked(dialog))

    return dialog

def suhuMenuTest():
    sQ.createSuhuDatabase()
    app = QtWidgets.QApplication(sys.argv)
    dialog = screenSuhu(0)
    dialog.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    suhuMenuTest()
