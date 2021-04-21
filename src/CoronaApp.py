from loginUI import startLogin as runApp
from initializedatabase import initializeDatabase as initDb
import sqlite3

conn = sqlite3.connect("sistem-tracking-corona.db")
c = conn.cursor()
try:
    c.execute("SELECT * FROM t_akun")
    c.execute("SELECT * FROM t_harian")
    c.execute("SELECT * FROM t_rs")
    conn.commit()
    conn.close()
except:
    conn.commit()
    conn.close()
    initDb()
runApp()