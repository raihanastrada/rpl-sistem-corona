from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import qtawesome as qta
import sys
import sqlite3

def kasusHarian():
    '''
    Tampilan Kasus Harian
    '''
    # initTableKasus()
    check()

    # Mengakses kasus terakhir
    latestCase = getLatestCase()
    print("Ini Latest Case")
    print(latestCase)

    app = QApplication(sys.argv)
    win = QWidget()
    loadUi('ScreenKasusHarian.ui', win)
    win.setWindowTitle("Kasus Harian COVID")

    # Label-label
    # Judul
    newText = win.label_0.text()+" ("+latestCase[0]+")"
    win.label_0.setText(newText)
    win.label_0.adjustSize()
    # Total Kasus
    newText = latestCase[1]
    win.label_2.setText(str(newText))
    win.label_2.adjustSize()
    # Jumlah Aktif
    newText = latestCase[2]
    win.label_4.setText(str(newText))
    win.label_4.adjustSize()
    # Jumlah Sembuh
    newText = latestCase[3]
    win.label_6.setText(str(newText))
    win.label_6.adjustSize()
    # Jumlah Meninggal
    newText = latestCase[4]
    win.label_8.setText(str(newText))
    win.label_8.adjustSize()

    # Button-button
    # Icons
    # '''
    # F13B6 = virus
    # F13B7 = virus-outline
    # F04D9 = stethoscope
    # F0FF6 = hospital -> sembuh
    # F068C = skull -> meninggal
    # F0BC8 = skull-outline
    # F0A42 = doctor -> dirawat
    # '''
    
    icon_virus = qta.icon('mdi.virus-outline',
    color='maroon')
    win.icon1.setIcon(icon_virus)
    win.icon1.setIconSize(QtCore.QSize(30,30))

    icon_stethoscope = qta.icon('mdi.stethoscope',
    color='navy',size=20)
    win.icon2.setIcon(icon_stethoscope)
    win.icon2.setIconSize(QtCore.QSize(30,30))

    icon_doctor = qta.icon('mdi.hospital',
    color='green')
    win.icon4.setIcon(icon_doctor)
    win.icon4.setIconSize(QtCore.QSize(30,30))

    icon_skull = qta.icon('mdi.skull-outline',
    color='black')
    win.icon3.setIcon(icon_skull)
    win.icon3.setIconSize(QtCore.QSize(30,30))

    # Button Back
    win.b1.clicked.connect(back)
    # Button Update
    win.b2.clicked.connect(formKasus)
    
    win.show()
    sys.exit(app.exec_())

def check():
    '''
    Buat ngecek isi tabel
    '''
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()

    c.execute("""
    SELECT *
    FROM t_harian
    """)

    records = c.fetchall()
    print(records)

    conn.commit()
    conn.close()

def initTableKasus():
    '''
    Menginisialisasi tabel kasus harian pada database
    '''
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS t_harian')
    c.execute("""
    CREATE TABLE t_harian (
        tanggal TEXT PRIMARY KEY,
        kasus_total INT(10),
        jumlah_aktif INT(10),
        jumlah_sembuh INT(10),
        jumlah_meninggal INT(10)
    );
    """)
    c.execute("""
    INSERT INTO t_harian
    VALUES
        ("2021-04-16",1594722,107297,1444229,43196),
        ("2021-04-17",1599763,106243,1450192,43328),
        ('2021-04-18', 1604348, 105859, 1455065, 43424);
    """)

    conn.commit()
    conn.close()

def back():
    '''
    b1 on click function, back to main menu
    '''
    widget = QWidget()
    loadUi('mainDialog.ui', widget)
    return widget

def formKasus():
    '''
    Tampilan form untuk memperbarui kasus
    '''
    form = QWidget()
    loadUi('FormUpdateKasus.ui', form)
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
            tanggal = form.dateEdit.date().toPyDate()
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
    msg.setDetailedText(e)
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
        c.execute("""
        UPDATE t_harian SET
        kasus_total = ?,
        jumlah_aktif = ?,
        jumlah_sembuh = ?,
        jumlah_meninggal = ?
        """, (entry[1], entry[2], entry[3], entry[4],) )
        print("Ini dari update data")
    else:
        # Belom ada -> Tambahin
        c.execute("INSERT INTO t_harian VALUES(?,?,?,?,?)", entry)
        c.execute("""
        SELECT *
        FROM t_harian
        """)
        print("Database Kasus Updated")
    conn.commit()
    conn.close()

def getLatestCase():
    '''
    Mengambil kasus terakhir pada database
    '''
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()

    c.execute("""
    SELECT *
    FROM t_harian
    ORDER BY (tanggal) DESC
    LIMIT 1
    """)

    records = c.fetchone()

    conn.commit()
    conn.close()

    '''
    tanggal = records[0]
    kasus_total = records[1]
    jumlah_aktif = records[2]
    jumlah_sembuh = records[3]
    jumlah_meninggal = records[4]
    '''
    return records

# kasusHarian()