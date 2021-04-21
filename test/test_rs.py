import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import rsQueries as rq
import loginQueries as lq
import sqlite3
import initializedatabase as initd

def test_init():
    initd.initializeDatabase()
    assert 1 == 1

def test_add_rs():
    rq.addRSEntry('dummyrs', 'Jl. dummyrs')
    rs_id = rq.getRSID('dummyrs')
    name = rq.getRSName(rs_id)
    listrs = rq.getAllRS()
    exist = rq.isAlamatExist('Jl. dummyrs')
    assert (len(listrs) > 0 and name == 'dummyrs' and exist == True)

def test_add_pemesanan():
    lq.addCustomerEntry('dummycustomer', 'dummycustomer@gmail.com', 
        'dummycustomer', 87712345, 2486)
    rq.addPemesananEntry('dummyrs', 'dummycustomer@gmail.com')
    rows = rq.getAllPesanan()
    assert len(rows) > 0