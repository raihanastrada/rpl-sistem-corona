import sqlite3
import loginQueries as lq

# Membuat tabel t_rs pada database dan mengembalikan koneksi ke database tersebut
def createRSDatabase():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS
                    t_rs(rs_id INTEGER PRIMARY KEY,
                    nama_rs TEXT NOT NULL UNIQUE,
                    alamat_rs TEXT NOT NULL UNIQUE,
                    status BOOLEAN NOT NULL DEFAULT TRUE
        )""")
    return cursor

# Membuat tabel t_prs pada database dan mengembalikan koneksi ke database tersebut
def createPemesananDatabase():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS
                    t_prs(order_id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    rs_id INTEGER NOT NULL,
                    timestamp_pesan TIMESTAMP DEFAULT (datetime('now','localtime')),
                    timestamp_review TIMESTAMP DEFAULT NULL,
                    timestamp_pembayaran TIMESTAMP DEFAULT NULL,
                    nominal_pembayaran INTEGER,
                    FOREIGN KEY (rs_id) REFERENCES t_rs(rs_id),
                    FOREIGN KEY (user_id) REFERENCES t_akun(user_id)
    )""")
    return cursor

# Mengembalikan True jika terdapat rumah sakit dengan alamat_rs = alamat pada database
# Mengembalikan False jika tidak terdapat
def isAlamatExist(alamat):
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT rs_id FROM t_rs WHERE alamat_rs = ?"
    cursor.execute(command, (alamat,))
    rows = cursor.fetchall()
    return len(rows) > 0

# Mengembalikan True jika terdapat rumah sakit dengan nama_rs = name pada database
# Mengembalikan False jika tidak terdapat
def isNameExist(name):
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT rs_id FROM t_rs WHERE nama_rs = ?"
    cursor.execute(command, (name,))
    rows = cursor.fetchall()
    return len(rows) > 0

# Mengembalikan True jika terdapat pemesanan dengan order_id = order_id pada database
# Mengembalikan False jika tidak terdapat
def isOrderExist(order_id):
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT user_id FROM t_prs WHERE order_id = ?"
    cursor.execute(command, (order_id,))
    rows = cursor.fetchall()
    return len(rows) > 0

# Mengembalikan seluruh rumah sakit yang terdapat pada database
def getAllRS():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM t_rs")
    rows = cursor.fetchall()
    return rows

# Mengembalikan rs_id dengan input nama_rs yang terdapat dalam database
# Mengembalikan False jika tidak terdapat rumah sakit dengan nama_rs = nama_rs pada database
def getRSID(nama_rs):
    if not isNameExist(nama_rs): return False
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT rs_id FROM t_rs WHERE nama_rs = ?"
    cursor.execute(command, (nama_rs,))
    rows = cursor.fetchall()
    return rows[0][0]

# Menambahkan data pada tabel t_rs pada database
# Input nama_rs dan alamat_rs dengan default status 1
def addRSEntry(nama_rs, alamat_rs):
    if (isNameExist(nama_rs)): return False
    if (isAlamatExist(alamat_rs)): return False
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    rs = (nama_rs, alamat_rs)
    command = """INSERT INTO t_rs(nama_rs, alamat_rs, timestamp_pesan)
                VALUES (?, ?, ?)"""
    cursor.execute(command, rs)
    cursor.connection.commit()
    return True

# Menambahkan data pemesanan pada tabel t_prs pada database
# Input nama_rs yang dipesan, email user yang memesan
def addPemesananEntry(nama_rs, email):
    if not isNameExist(nama_rs): return False
    if not lq.isEmailExist(email): return False
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    user_id = lq.getUserID(email)
    rs_id = getRSID(nama_rs)
    add = (user_id, rs_id)
    print(add)
    command = """INSERT INTO t_prs(user_id, rs_id)
                VALUES (?, ?)"""
    cursor.execute(command, add)
    cursor.connection.commit()
    return True

# Mendapatkan seluruh pesanan yang terdapat pada tabel t_prs
def getAllPesanan():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM t_prs")
    rows = cursor.fetchall()
    if len(rows) == 0: return False
    return rows

# Mendapatkan seluruh pesanan yang terdapat pada tabel t_prs yang belum direview
# Mengembalikan False jika tidak terdapat pesanan yang belum direview
def getAllPesananNotReviewed():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM t_prs WHERE timestamp_review IS NULL")
    rows = cursor.fetchall()
    if len(rows) == 0: return False
    return rows

# Meng-update entry pada tabel pesanan untuk mendandakan sudah direview oleh admin
# Mengembalikan False jika tidak terdapat order_id dan True jika berhasil mengupdate
def setPesananReviewed(order_id):
    if not isOrderExist(order_id): return False
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """UPDATE t_prs
                SET timestamp_review = datetime('now','localtime')
                WHERE order_id = ?"""
    cursor.execute(command, (order_id,))
    cursor.connection.commit()
    return True

# Mendapatkan pesanan user yang sedang dalam proses (proses review atau belum dibayar)
# Mengembalikan False jika tidak terdapat pesanan yang sedang dalam proses
def getOngoingPesananUser(email):
    if not lq.isEmailExist(email): return False
    uid = lq.getUserID(email)
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """SELECT * FROM t_prs
                WHERE timestamp_pembayaran IS NULL 
                AND user_id = ?"""
    cursor.execute(command, (uid,))
    rows = cursor.fetchall()
    if len(rows) == 0: return False
    return rows

# Meng-update pesanan pada tabel t_prs dalam database untuk menandakan sudah terbayar
def setPesananPaid(order_id):
    if not isOrderExist(order_id): return False
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """UPDATE t_prs
                SET timestamp_pembayaran = datetime('now','localtime')
                WHERE order_id = ?"""
    cursor.execute(command, (order_id,))
    cursor.connection.commit()
    return True

# Mendapatkan nama rumah sakit pada database dengan input rs_id
def getRSName(rs_id):
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT nama_rs FROM t_rs WHERE rs_id = ?"
    cursor.execute(command, (rs_id,))
    rows = cursor.fetchall()
    return rows[0][0]

# Menghapus entry pemesanan pada tabel t_prs berdasarkan order_id
# Digunakan untuk menolak atau me-reject pemesanan
# False jika tidak ada order_id yang sesuai, True jika berhasil dihapus
def deletePemesananEntry(order_id):
    if not isOrderExist(order_id): return False
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """DELETE FROM t_prs WHERE order_id = ?"""
    cursor.execute(command, (order_id,))
    cursor.connection.commit()
    return True

# Mengembalikan True jika terdapat pemesanan dengan order_id = order_id dan belum direview
# mengembalikan False jika tidak ada
def isNotReviewed(order_id):
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT user_id FROM t_prs WHERE order_id = ? and timestamp_review IS NULL"
    cursor.execute(command, (order_id,))
    rows = cursor.fetchall()
    return len(rows) > 0
    
if __name__ == "__main__":
    print("running rsQueries")
    createRSDatabase()
    createPemesananDatabase()
    addRSEntry('Jakarta Hospital', 'Jl. Jend. Sudirman No. Kav 49')
    addRSEntry('Rumah Sakit Jakarta', 'Jl. Garnisun No. 1 Karet Semanggi Setia Budi')
    addRSEntry('Jakarta Islamic Hospital', 'Jl. Cemp. Putih Tengah I No. 1')
    addRSEntry('Gatot Subroto', 'Jl. Abdul Rahman Saleh 24')
    addRSEntry('Gatot Subroto', 'Jl. Abdul Rahman Saleh 24')
    addRSEntry('Rumah Sakit Cikini', 'Jl. Raden Saleh Raya No.40')
    addRSEntry('Abdi Waluyo Hospital', 'Jl. HOS. Cokroaminoto No.31-33')
    addRSEntry('RS Bunda Jakarta', 'Jl. Teuku Cik Ditiro 1 No.11')
    addRSEntry('Royal Taruma Hospital', 'Daan Mogot Rd Kedaung No.34')
    print(getAllRS())
    # addPemesananEntry('Jakarta Hospital', 'nolercustomer@gmail.com')
    print(getAllPesanan())
    print(getAllPesananNotReviewed())
    setPesananReviewed(1)
    print(getAllPesanan())
    print(getAllPesananNotReviewed())
    print(getOngoingPesananUser('nolercustomer@gmail.com'))
    setPesananPaid(1)
    print(getAllPesanan())
    print(getAllPesananNotReviewed())
    print(getOngoingPesananUser('nolercustomer@gmail.com'))
