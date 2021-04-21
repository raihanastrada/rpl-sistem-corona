import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from membership import *
import sqlite3
import loginQueries as lq
import initializedatabase as initd
import datetime
from dateutil.relativedelta import relativedelta

def test_init():
    initd.initializeDatabase()
    assert 1 == 1

def test_getmembershipstatus_nonmember():
    # Mengecek apakah program berhasil
    # mendapatkan hasil yang tepat
    # untuk status membership customer
    lq.addCustomerEntry('dummycustomermember', 'dummycustomermember@gmail.com', 
        'dummycustomer', 87881528377, 2486)
    email = 'dummycustomermember@gmail.com'
    records = getMembershipStatus(email)
    assert (records[0] == False and records[1] == str(datetime.date.today()))

def test_updatetomember():
    # Mengecek apakah program berhasil
    # memperbarui status membership dari
    # sebuah akun yang terdaftar sebagai customer
    lq.addCustomerEntry('dummycustomermember', 'dummycustomermember@gmail.com', 
        'dummycustomer', 87881528377, 2486)
    email = 'dummycustomermember@gmail.com'
    updateMembershipStatus(email, 12)
    records = getMembershipStatus(email)
    assert (records[0] == True)