import sys
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic import loadUi
import loginQueries as lq

# def backButton_clicked():
#     # backButton on click function, back to main menu
#     print("backButton clicked")
#     widget = QWidget()
#     loadUi('mainDialog.ui', widget)
#     return widget

def getMembershipStatus(email):
    # if not isEmailExist(email): return "None", "None"
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """SELECT t_customer.membership_status > CURRENT_DATE,
                t_customer.membership_status
                FROM t_akun JOIN t_customer
                ON t_akun.user_id = t_customer.user_id
                WHERE email = ?"""
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    if len(rows) == 0: return "None", "None"
    return bool(rows[0][0]), rows[0][1]

def membershipWindow(email):
    # Tampilan awal Fitur Membership
    win = QWidget()
    loadUi('screens/MembershipScreen.ui', win)
    win.setWindowTitle("Membership")

    # Label-label
    records = getMembershipStatus(email)
    # Membership Status
    win.status_Label.setText(str(records[0]))
    # Membership Validity Date
    win.date_Label.setText(str(records[1]))

    # Button-button
    # Back Button
    # win.backButton.clicked.connect(backButton_clicked)
    win.backButton.setVisible(False)
    # Get Membership Button
    win.getMembershipButton.clicked.connect(lambda: buyMembershipWindow(email))
    
    win.show()
    return win

def buyMembershipWindow(email):
    # Tampilan layar pembelian Membership
    form = QWidget()
    loadUi('screens/BuyMembershipScreen.ui', form)
    form.setWindowTitle("Buy Membership")
    filled = set()

    form.lineEdit.textChanged.connect(lambda: filled.add("lineEdit"))
    form.buyButton.clicked.connect(lambda: processBuyMembership(email, form, filled))
    
    form.show()

def processBuyMembership(email, form, filled):
    res = confirmBuyMsg()
    # print(res)
    if(res == 0):
        try:
            monthEntry = int(form.lineEdit.text())
            # print("Memasukkan data", end=" ")
            # print(monthEntry)
            updateMembershipStatus(email, monthEntry)
            successBuyMsg()

            form.lineEdit.clear()
            filled.clear()
            form.close()

        except Exception as e:
            errorBuyMsg(repr(e))

def updateMembershipStatus(email, entry):
    connection = sqlite3.connect("sistem-tracking-corona.db")
    cursor = connection.cursor()
    command = """
    SELECT membership_status
    FROM t_akun JOIN t_customer
    ON t_akun.user_id = t_customer.user_id
    WHERE email = ?
    """
    cursor.execute(command, (email,))
    check = cursor.fetchall()
    # print(check)
    if check:
        x = "+" + str(entry) + " months"
        command = """UPDATE t_customer 
        SET membership_status = DATE(membership_status, ?)
        WHERE user_id IN
        (
            SELECT t_customer.user_id
            FROM t_customer INNER JOIN t_akun
            ON t_customer.user_id = t_akun.user_id
            WHERE email = ?
        )"""
        cursor.execute(command, (x, email,))
        # print("success")
    connection.commit()
    connection.close()

def confirmBuyMsg():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setWindowTitle("Konfirmasi Pembelian Membership")
    msg.setText("Apakah anda yakin ingin membeli Membership?")
    msg.addButton("Ya", QMessageBox.YesRole)
    msg.addButton("Tidak", QMessageBox.NoRole)
    msg.setDefaultButton(QMessageBox.No)

    res = msg.exec_()
    return res

def errorBuyMsg(e):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Error")
    msg.setText("Terdapat kesalahan saat pengisian form")
    msg.setDetailedText(e)
    msg.exec_()

def successBuyMsg():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Pembelian Membership")
    msg.setText("Pembelian Membership Berhasil Dilakukan")
    msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    membershipWindow('nolercustomer@gmail.com')
    sys.exit(app.exec_())