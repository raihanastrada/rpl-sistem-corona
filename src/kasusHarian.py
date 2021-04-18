from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import sqlite3

def back():
    '''
    b1 on click function, back to main menu
    '''
    print("Back")

def window():
    '''
    Main Window
    '''
    # Mengakses kasus terakhir
    latestCase = getLatestCase()
    print("Ini Latest Case")
    print(latestCase)

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(300, 300, 400, 400) # xpos,ypos,width,height
    win.setWindowTitle("Kasus Harian COVID")

    # Label-label buat nampilin kasus
    label = QtWidgets.QLabel(win)
    label.setText("kasus meninggal")
    label.adjustSize()
    label.move(75,75)

    # Button Back
    b1 = QtWidgets.QPushButton(win)
    b1.setText("Kembali")
    b1.move(10,10)
    b1.clicked.connect(back)

    # Button Update
    b2 = QtWidgets.QPushButton(win)
    b2.setText("Update Kasus COVID")
    label.adjustSize()
    b2.move(250,250)
    entry = ("20210417",1599763,106243,1450192,43328)
    b2.clicked.connect(lambda: updateCase(entry))

    win.show()
    sys.exit(app.exec_())

# icons
'''
F13B6 = virus
F13B7 = virus-outline
F04D9 = mdi-stethoscope
F0FF6 = hospital -> sembuh
F068C = skull -> meninggal
F0BC8 = skull-outline
F0A42 = mdi-doctor -> dirawat
'''

def confirm_msg():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)

    msg.setText("Apakah anda yakin ingin mengupdate data?")
    msg.addButton("Ya", QMessageBox.YesRole)
    msg.addButton("Tidak", QMessageBox.NoRole)
    msg.setDefaultButton(QMessageBox.No)

    res = msg.exec_()
    return res == 0

# def createdb():
#     conn = sqlite3.connect("sistem-tracking-corona.db")
#     c = conn.cursor()
#     c.execute("SELECT * FROM t_harian")
#     records = c.fetchall()
#     print(records)
#     c.execute('DROP TABLE IF EXISTS t_harian')
#     c.execute("""
#     CREATE TABLE t_harian (
#         tanggal TEXT PRIMARY KEY,
#         kasus_total INT(10),
#         jumlah_aktif INT(10),
#         jumlah_sembuh INT(10),
#         jumlah_meninggal INT(10)
#     );
#     """)
#     c.execute("""
#     INSERT INTO t_harian
#     VALUES
#         ("20210416",1594722,107297,1444229,43196);
#     """)
#     c.execute("""
#     INSERT INTO t_harian
#     VALUES
#         ("20210417",1599763,106243,1450192,43328);
#     """)

#     conn.commit()
#     conn.close()

def updateCase(entry):
    '''
    Masukin entry ke database t_harian
    '''
    # Konfirmasi
    if (confirm_msg()):
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

    else:
        print("Ini karena ditolak")

def getLatestCase():
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

window()