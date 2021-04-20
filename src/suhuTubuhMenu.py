from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
import suhuQueries as sQ

def submitSuhu_clicked(dialog):
    if (not sQ.addSuhuEntry(int(dialog.userid.text()), dialog.inputTanggalDateEdit.date(), float(dialog.inputSuhuLineEdit.text()))):
        dialog.message.setText("Error uploading to database")
    return

def lihatRiwayat_clicked(dialog):
    result = sQ.getRiwayatSuhuTubuh(int(dialog.userid.text()), dialog.dariTanggalDateEdit.date(), dialog.sampaiTanggalDateEdit.date())
    if (not result):
        dialog.message.setText("Error getting temperature history")
    else:
        dialog.tableWidget.setRowCount(0)
        for i in range(len(result)):
            dialog.tableWidget.setItem(i, 0, result[i][0])
            dialog.tableWidget.setItem(i, 1, result[i][1])
            dialog.tableWidget.setItem(i, 2, sQ.evaluasiSuhu(result[i][1]))
    return

def screenSuhu(user_id):
    dialog = QtWidgets.QDialog()
    loadUi('suhuTubuhMenu.ui')

    dialog.setWindowTitle("Suhu Tubuh")
    dialog.userid.setText(user_id)
    dialog.inputSuhuLineEdit.setValidator(QtGui.QDoubleValidator())

    dialog.submitSuhu.clicked.connect(lambda: submitSuhu_clicked)
    dialog.lihatRiwayat.clicked.connect(lambda: lihatRiwayat_clicked)

    return dialog

def suhuMenuTest():
    app = QtWidgets.QApplication(sys.argv)
    dialog = screenSuhu(0)
    dialog.show()
    sys.exit(app.exec_())
    return

if _name__ == "__main__":
    suhuMenuTest()
