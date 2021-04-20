import pytest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from kasusHarian import *
import sqlite3

# # Kasus Harian
# def test5_1():
#     '''
#     Mengecek apakah program dapat menjalankan
#     layar kasus harian untuk admin
#     '''
#     compiled = True
#     try:
#         kasusHarian(True)
#     except:
#         compiled = False
#     assert (compiled)

# def test5_2():
#     '''
#     Mengecek apakah program dapat menjalankan
#     layar kasus harian untuk customer
#     '''
#     compiled = True
#     try:
#         kasusHarian(False)
#     except:
#         compiled = False
#     assert (compiled)

# Menampilkan Kasus Harian
def test_61():
    '''
    Mengecek apakah program dapat mengambil
    kasus terakhir pada database
    '''
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    # Mengambil jawaban terakhir
    c.execute("""
    SELECT *
    FROM t_harian
    ORDER BY (tanggal) DESC
    LIMIT 1
    """)
    answer = c.fetchone()
    conn.commit()
    conn.close()

    # Menggunakan fungsi getLatestCase()
    case = getLatestCase()

    assert(answer==case)

dummy_entry_na = ('9999-99-99',0,0,0,0)
dummy_entry_a = ("2021-04-16",1,1,1,1)
dummy_entry_err1 = ("9999-99-99",None,None,None,None)
dummy_entry_err2 = ("9999-99-99","None","None","None","None")

# Update Kasus Harian
# Nambah di database
def test_71():
    '''
    Mengecek apakah program dapat 
    menambahkan entri ke database, 
    kasus belum terdapat pada db
    '''
    initTableKasus()
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    # Mengambil jawaban terakhir
    c.execute("""
    SELECT *
    FROM t_harian
    """)
    answer = c.fetchall()
    conn.commit()
    conn.close()
    n = 0
    if answer:
        n = len(answer)
    updateCase(dummy_entry_na)
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    # Mengambil jawaban terakhir
    c.execute("""
    SELECT *
    FROM t_harian
    """)
    record = c.fetchall()
    conn.commit()
    conn.close()
    m = len(record)
    assert (m == n+1)

    initTableKasus()

# Kasus sudah terdapat di database
def test_72():
    '''
    Mengecek apakah program dapat 
    menambahkan entri ke database, 
    kasus sudah terdapat pada db
    '''
    initTableKasus()
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    c.execute("""
    SELECT *
    FROM t_harian
    """)
    answer = c.fetchall()
    conn.commit()
    conn.close()
    # n = 0
    if answer:
        n = len(answer)
    updateCase(dummy_entry_a)
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    c.execute("""
    SELECT *
    FROM t_harian
    """)
    answer = c.fetchall()
    conn.commit()
    conn.close()
    m = len(answer)
    assert (m == n)

    initTableKasus()

# Kasus pengisian form belum selesai
def test_73():
    initTableKasus()
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    # Mengambil jawaban terakhir
    c.execute("""
    SELECT *
    FROM t_harian
    """)
    answer = c.fetchall()
    conn.commit()
    conn.close()
    n = 0
    if answer:
        n = len(answer)
    updateCase(dummy_entry_err1)
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    # Mengambil jawaban terakhir
    c.execute("""
    SELECT *
    FROM t_harian
    """)
    answer = c.fetchall()
    conn.commit()
    conn.close()
    m = len(answer)
    assert (m == n)

    initTableKasus()

# Kasus pengisian form tidak memasukkan angka
def test_74():
    initTableKasus()
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    # Mengambil jawaban terakhir
    c.execute("""
    SELECT *
    FROM t_harian
    """)
    answer = c.fetchall()
    conn.commit()
    conn.close()
    n = 0
    if answer:
        n = len(answer)
    updateCase(dummy_entry_err2)
    conn = sqlite3.connect("sistem-tracking-corona.db")
    c = conn.cursor()
    # Mengambil jawaban terakhir
    c.execute("""
    SELECT *
    FROM t_harian
    """)
    answer = c.fetchall()
    conn.commit()
    conn.close()
    m = len(answer)
    assert (m == n)

    initTableKasus()

# def runTC():
#     test5_1()
#     test5_2()
#     test6_1()
#     test6_2()
#     test7_1()
#     test7_2()
#     test7_3()
#     test7_4()
