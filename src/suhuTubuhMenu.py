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
    widget = QtWidgets.QWidget()
    loadUi('screens/SuhuTubuhMenuScreen.ui', widget)

    widget.setWindowTitle("Suhu Tubuh")
    widget.userid.setText(str(user_id))
    widget.inputSuhuLineEdit.setValidator(QtGui.QDoubleValidator())

    widget.submitSuhu.clicked.connect(lambda: submitSuhu_clicked(widget))
    widget.lihatRiwayat.clicked.connect(lambda: lihatRiwayat_clicked(widget))

    return widget

def suhuMenuTest(userid):
    sQ.createSuhuDatabase()
    app = QtWidgets.QApplication(sys.argv)

    ### UBAH PAS DEPLOY
    dialog = screenSuhu(userid)
    dialog.show()
    sys.exit(app.exec_())
    return

if __name__ == "__main__":
    ### SET USER ID PLS
    suhuMenuTest() 
