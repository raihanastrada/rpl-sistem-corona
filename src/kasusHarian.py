from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import formKasusHarian as fkh
import qtawesome as qta
import sys
import sqlite3

def kasusHarian(admin):
    '''
    Tampilan Kasus Harian
    '''
    # Test
    # initTableKasus()
    # createTableKasus()
    check()

    # Mengakses kasus terakhir
    latestCase = getLatestCase()
    print("Ini Latest Case")
    print(latestCase)

    # app = QApplication(sys.argv)
    win = QWidget()
    try:
        loadUi('../screens/KasusHarianScreen.ui', win)
    except:
        loadUi('screens/KasusHarianScreen.ui', win)
    win.setWindowTitle("Kasus Harian COVID")

    # Label-label
    # Judul
    # 2021/04/19
    if not latestCase:
        win.label_2.setText("-")
        win.label_2.adjustSize()

        win.label_4.setText("-")
        win.label_4.adjustSize()

        win.label_6.setText("-")
        win.label_6.adjustSize()

        win.label_8.setText("-")
        win.label_8.adjustSize()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error")

        text = "tunggu admin memperbarui data kasus harian"
        if (admin):
            text = "Update Kasus Harian"
        msg.setText("Tidak terdapat kasus harian, " + text)
        msg.exec_()
    else:
        tanggal_indo = latestCase[0][8:10]+"/"+latestCase[0][5:7]+"/"+latestCase[0][0:4]
        newText = win.label_0.text()+" ("+tanggal_indo+")"
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
    # win.b1.clicked.connect(back)
    win.b1.setVisible(False)
    # Button Update
    if (admin):
        win.b2.clicked.connect(lambda: fkh.formKasus(win))
    else:
        win.b2.setVisible(False)
        
    win.show()
    return win
    # sys.exit(app.exec_())

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
    print("Isi Data t_harian: ")
    print(records)

    conn.commit()
    conn.close()

def createTableKasus():
    '''
    Membuat tabel kasus harian kosong pada database
    '''
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS t_harian')
    c.execute("""
    CREATE TABLE t_harian (
        tanggal DATE PRIMARY KEY,
        kasus_total INT(10),
        jumlah_aktif INT(10),
        jumlah_sembuh INT(10),
        jumlah_meninggal INT(10)
    );
    """)

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
        tanggal DATE PRIMARY KEY,
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
        ('2021-04-18',1604348,105859,1455065,43424),
        ('2021-04-19',1609300,104319,1461414,43567);
    """)

    conn.commit()
    conn.close()

# def back():
#     '''
#     b1 on click function, back to main menu
#     '''
#     widget = QWidget()
#     loadUi('mainDialog.ui', widget)
#     return widget

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kasusHarian('adminnoler@gmail.com')
    sys.exit(app.exec_())