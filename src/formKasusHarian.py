from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import kasusHarian as kh
import sys
import sqlite3

def formKasus():
    '''
    Tampilan form untuk memperbarui kasus
    '''
    form = QWidget()
    loadUi('screens/UpdateKasusScreen.ui', form)
    form.setWindowTitle("Form Update Kasus COVID")
    filled = set()

    form.dateEdit.dateChanged.connect(lambda: filled.add("dateEdit"))
    form.lineEdit.textChanged.connect(lambda: filled.add("lineEdit"))
    form.lineEdit2.textChanged.connect(lambda: filled.add("lineEdit2"))
    form.lineEdit3.textChanged.connect(lambda: filled.add("lineEdit3"))
    form.lineEdit4.textChanged.connect(lambda: filled.add("lineEdit4"))

    form.b1.clicked.connect(lambda: processForm(form, filled))

    form.show()

def processForm(form, filled):
    '''
    Mengkonfirmasi pengisian form dan mengecek apakah isi form valid
    '''
    res = confirm_msg()
    print(res)
    if(res==0):
        try:
            isFormFilled(filled)
            print("awal")
            print(form.dateEdit.date())
            print(type(form.dateEdit.date()))
            tanggal = form.dateEdit.date().toPyDate()
            print("akhir")
            print(tanggal)
            print(type(tanggal))
            entry = (tanggal, int(form.lineEdit.text()), int(form.lineEdit2.text()), int(form.lineEdit3.text()), int(form.lineEdit4.text()))
            print("Memasukkan data",end=" ")
            print(entry)
            updateCase(entry)
            notif_msg()

            date = QtCore.QDate(2000,1,1);
            form.dateEdit.setDate(date)
            form.lineEdit.clear()
            form.lineEdit2.clear()
            form.lineEdit3.clear()
            form.lineEdit4.clear()
            filled.clear()

            form.close()

        except Exception as e:
            error_msg(repr(e))

def isFormFilled(filled):
    '''
    Mengecek apakah seluruh form telah terisi
    '''
    edits = ["dateEdit", "lineEdit", "lineEdit2", "lineEdit3", "lineEdit4"]
    
    for el in edits:
        if el not in filled: raise Exception("Terdapat bagian dari form yang belum terisi")

# MessageBox    
def confirm_msg():
    '''
    Menampilkan Konfirmasi Pengisian Form Data Kasus
    '''
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setWindowTitle("Konfirmasi Update Data COVID")
    msg.setText("Apakah anda yakin ingin mengupdate data?")
    msg.addButton("Ya", QMessageBox.YesRole)
    msg.addButton("Tidak", QMessageBox.NoRole)
    msg.setDefaultButton(QMessageBox.No)

    res = msg.exec_()
    return res

def error_msg(e):
    '''
    Menampilkan pesan dan detail error saat pengisian form
    '''
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Error")

    msg.setText("Terdapat kesalahan saat pengisian form")
    # if (e.ValueError):
    #     msg.setDetailedText("TEST")
    msg.exec_()

def notif_msg():
    '''
    Menampilkan pemberitahuan data kasus harian berhasil diperbarui
    '''
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Pesan")
    
    msg.setText("Data Kasus Harian Berhasil Diperbarui")
    msg.exec_()
    
def updateCase(entry):
    '''
    Memasukkan entry ke database t_harian
    '''
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    c.execute("""
    SELECT *
    FROM t_harian
    WHERE tanggal = ?
    """, (entry[0],))
    result = c.fetchone()
    print("Ini ngecek ada atau gak")
    if result:
        # Udah ada di database -> Update yang lama
        try:
            int(entry[1])
            int(entry[2])
            int(entry[3])
            int(entry[4])
            c.execute("""
            UPDATE t_harian SET
            kasus_total = ?,
            jumlah_aktif = ?,
            jumlah_sembuh = ?,
            jumlah_meninggal = ?,
            WHERE tanggal = ?
            """, (entry[1], entry[2], entry[3], entry[4],entry[0],) )
            print("Ini dari update data")
            print("Jadi gini")
        except:
            print("")
    else:
        # Belom ada -> Tambahin
        try:
            int(entry[1])
            int(entry[2])
            int(entry[3])
            int(entry[4])
            c.execute("INSERT INTO t_harian VALUES(?,?,?,?,?)", entry)
            c.execute("""
            SELECT *
            FROM t_harian
            """)
            print("Database Kasus Updated")
        except:
            print("")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    formKasus()