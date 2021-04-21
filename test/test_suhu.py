import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import suhuQueries as sq
import loginQueries as lq
import sqlite3
import initializedatabase as initd
import datetime
from PyQt5.QtCore import QDate

def test_init():
    initd.initializeDatabase()
    assert 1 == 1

def test_suhu():
    lq.addCustomerEntry('dummycustomer', 'dummycustomer@gmail.com', 
        'dummycustomer', 87881528311, 2486)
    email = 'dummycustomer@gmail.com'
    user_id = lq.getUserID(email)
    date = QDate.fromString('2021-04-20', 'yyyy-mm-dd')
    sq.addSuhuEntry(user_id, date, 36)
    assert (sq.isSuhuExist(user_id, date) == True)

def test_normalitas():
    hasil = sq.evaluasiSuhu(100)
    assert (hasil == "Abnormal")

def test_normal():
    hasil = sq.evaluasiSuhu(36)
    assert (hasil == "Normal")