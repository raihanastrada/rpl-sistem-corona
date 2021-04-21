import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import loginQueries as lq
import sqlite3
import initializedatabase as initd

def test_init():
    initd.initializeDatabase()
    assert 1 == 1

# Test untuk mendapatkan nama yang benar
def test_login_1():
    nama = lq.getName('adminnoler@gmail.com')
    assert nama == 'Admin Noler'

# Test untuk mendapatkan user id yang benar
def test_login_2():
    user_id = lq.getUserID('adminnoler@gmail.com')
    assert user_id == 1

# Test untuk mengecek fungsi menambahkan admin
def test_add_admin():
    lq.addAdminEntry('dummyadmin', 'dummyadmin@gmail.com', 'dummyadmin', 8771234)
    email = 'dummyadmin@gmail.com'
    name = lq.getName(email)
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """DELETE FROM t_akun WHERE email = ?"""
    cursor.execute(command, (email,))
    cursor.connection.commit()
    assert name == 'dummyadmin'

# Mengetest untuk mengecek penambahan customer benar atau tidak
def test_add_customer():
    lq.addCustomerEntry('dummycustomer', 'dummycustomer@gmail.com', 
        'dummycustomer', 87712345, 2486)
    email = 'dummycustomer@gmail.com'
    name = lq.getName(email)
    user_id = lq.getUserID(email)
    upin = lq.getPIN(email)
    mem_status = lq.getMembershipStatus(email)
    assert (name == 'dummycustomer' and upin == 2486 and mem_status[0] == False)
