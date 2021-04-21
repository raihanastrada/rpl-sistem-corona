import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from membership import *
import sqlite3

dummy_customer_member = 'nolercustomer@gmail.com'
dummy_customer_nonmember = 'customernoler@gmail.com'
dummy_admin = 'adminmaxi@gmail.com'
dummy_entry = '5'

def test_get_status_member():
    '''
    Mengecek apakah program berhasil
    mendapatkan status membership
    dari akun yang terdaftar sebagai customer 
    dan sudah merupakan member
    '''
    connection = sqlite3.connect("sistem-tracking-corona.db")
    cursor = connection.cursor()
    command = """SELECT t_customer.membership_status > CURRENT_DATE,
                t_customer.membership_status
                FROM t_akun JOIN t_customer
                ON t_akun.user_id = t_customer.user_id
                WHERE email = ?"""
    cursor.execute(command, (dummy_customer_member,))
    rows = cursor.fetchall()
    answer1 = bool(rows[0][0])
    answer2 = rows[0][1]
    records = getMembershipStatus(dummy_customer_member)
    assert(answer1 == records[0] and answer2 == records[1])

def test_get_status_nonmember():
    '''
    Mengecek apakah program berhasil
    mendapatkan status membership
    dari akun yang terdaftar sebagai customer 
    tetapi bukan merupakan member
    '''
    connection = sqlite3.connect("sistem-tracking-corona.db")
    cursor = connection.cursor()
    command = """SELECT t_customer.membership_status > CURRENT_DATE,
                t_customer.membership_status
                FROM t_akun JOIN t_customer
                ON t_akun.user_id = t_customer.user_id
                WHERE email = ?"""
    cursor.execute(command, (dummy_customer_nonmember,))
    rows = cursor.fetchall()
    answer1 = bool(rows[0][0])
    answer2 = rows[0][1]
    records = getMembershipStatus(dummy_customer_nonmember)
    assert(answer1 == records[0] and answer2 == records[1])

def test_get_status_admin():
    '''
    Mengecek apakah program berhasil
    mendapatkan status membership
    dari akun yang terdaftar sebagai admin
    '''
    connection = sqlite3.connect("sistem-tracking-corona.db")
    cursor = connection.cursor()
    command = """SELECT t_customer.membership_status > CURRENT_DATE,
                t_customer.membership_status
                FROM t_akun JOIN t_customer
                ON t_akun.user_id = t_customer.user_id
                WHERE email = ?"""
    cursor.execute(command, (dummy_admin,))
    rows = cursor.fetchall()
    answer1 = bool(rows[0][0])
    answer2 = rows[0][1]
    records = getMembershipStatus(dummy_admin)
    assert(answer1 == records[0] and answer2 == records[1])

def test_update_status():
    '''
    Mengecek apakah program berhasil
    memperbarui status membership dari
    sebuah akun yang terdaftar sebagai customer
    '''
    connection = sqlite3.connect("sistem-tracking-corona.db")
    cursor = connection.cursor()
    command = """
    SELECT membership_status
    FROM t_akun JOIN t_customer
    ON t_akun.user_id = t_customer.user_id
    WHERE email = ?
    """
    cursor.execute(command, (dummy_customer_member,))
    check = cursor.fetchall()
    connection.commit()
    connection.close()

    updateMembershipStatus(dummy_customer_member, dummy_entry)

    connection = sqlite3.connect("sistem-tracking-corona.db")
    cursor = connection.cursor()
    command = """
    SELECT membership_status
    FROM t_akun JOIN t_customer
    ON t_akun.user_id = t_customer.user_id
    WHERE email = ?
    """
    cursor.execute(command, (dummy_customer_member,))
    answer = cursor.fetchall()
    connection.commit()
    connection.close()
    '''
    membership_status dari sebelum dan setelah pembaharuan
    tidak akan sama
    '''
    assert(answer != check)