from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import qtawesome as qta
import sys
import sqlite3

def back():
    '''
    b1 on click function, back to main menu
    '''
    print("Back")

def kasusHarian():
    '''
    Main Window
    '''
    # Mengakses kasus terakhir
    latestCase = getLatestCase()
    print("Ini Latest Case")
    print(latestCase)

    app = QApplication(sys.argv)
    win = QWidget()
    loadUi('ScreenKasusHarian.ui', win)
    win.setWindowTitle("Kasus Harian COVID")
    form = QWidget()
    loadUi('FormUpdateKasus.ui', form)
    form.setWindowTitle("Form Update Kasus COVID")

    # Label-label
    # Judul
    newText = win.label_0.text()+" "+latestCase[0]
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
    # Icon
    icon_virus = qta.icon('mdi.virus-outline',
    color='black')
    win.icon1.setIcon(icon_virus)
    icon_stethoscope = qta.icon('mdi.stethoscope',
    color='black')
    win.icon2.setIcon(icon_stethoscope)
    icon_hospital = qta.icon('mdi.hospital',
    color='black')
    win.icon3.setIcon(icon_hospital)
    icon_skull = qta.icon('mdi.skull-outline',
    color='black')
    win.icon3.setIcon(icon_skull)
    icon_doctor = qta.icon('mdi.doctor',
    color='black')
    win.icon4.setIcon(icon_doctor)
    # Button Back
    win.b1.clicked.connect(back)
    # Button Update
    entry = ("20210417",1599763,106243,1450192,43328)
    win.b2.clicked.connect(lambda: updateCaseForm(form, entry))
    
    win.show()
    sys.exit(app.exec_())

# icons
'''
F13B6 = virus
F13B7 = virus-outline
F04D9 = stethoscope
F0FF6 = hospital -> sembuh
F068C = skull -> meninggal
F0BC8 = skull-outline
F0A42 = doctor -> dirawat
'''

def confirm_msg(result):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setWindowTitle("Konfirmasi Update Data COVID")
    
    msg.setText("Apakah anda yakin ingin mengupdate data?")
    msg.addButton("Ya", QMessageBox.YesRole)
    msg.addButton("Tidak", QMessageBox.NoRole)
    msg.setDefaultButton(QMessageBox.No)

    res = msg.exec_()
    if (res==0): result = True
    
    print("Akhir")
    print(result)


def error_msg(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Error")

    msg.setText("Terdapat kesalahan saat pengisian form")
    msg.setDetailedText(e)
    msg.exec_()

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

def isFormFilled(filled):
    edits = ["dateEdit", "lineEdit", "lineEdit2", "lineEdit3", "lineEdit4"]
    
    for el in edits:
        if el not in filled: raise Exception("Terdapat bagian dari form yang belum terisi")
    return True

def processForm(form, filled):
    print("test")
    res = False
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)

    msg.setText("Apakah anda yakin ingin mengupdate data?")
    msg.addButton("Ya", QMessageBox.YesRole)
    msg.addButton("Tidak", QMessageBox.NoRole)
    msg.setDefaultButton(QMessageBox.No)

    res = msg.exec_()
    if(res==0):
        try:
            isFormFilled(filled)
            print("bruh")
            print(type(form.dateEdit.date().toPyDate()))
            tanggal = form.dateEdit.date().toPyDate()
            print(tanggal)
            entry = (tanggal, int(form.lineEdit.text()), int(form.lineEdit2.text()), int(form.lineEdit3.text()), int(form.lineEdit4.text()))
            updateCase(entry)

        except Exception as e:
            error_msg(repr(e))
            
    form.close()
    

def updateCaseForm(form, entry):
    # res = False
    form.show()
    filled = set()

    form.dateEdit.dateChanged.connect(lambda: filled.add("dateEdit"))
    form.lineEdit.textChanged.connect(lambda: filled.add("lineEdit"))
    form.lineEdit2.textChanged.connect(lambda: filled.add("lineEdit2"))
    form.lineEdit3.textChanged.connect(lambda: filled.add("lineEdit3"))
    form.lineEdit4.textChanged.connect(lambda: filled.add("lineEdit4"))

    form.b1.clicked.connect(lambda: processForm(form, filled))

    # if(res):
    #     print(form.lineEdit.text())
    #     print(type(form.lineEdit.text()))
    #     print(form.lineEdit2.text())
    #     print(type(form.lineEdit2.text()))
    #     print(form.dateEdit.text())
    #     print(type(form.dateEdit.text()))
    #     # updateCase()

    # form.close()

def updateCase(entry):
    '''
    Masukin entry ke database t_harian
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

kasusHarian()