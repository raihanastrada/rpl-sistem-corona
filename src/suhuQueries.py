import sqlite3

# Membuat tabel t_suhu pada database dan mengembalikan koneksi ke database tersebut
def createSuhuDatabase():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        t_suhu(
            user_id INTEGER,
            tanggal DATE,
            suhu FLOAT NOT NULL,
            CONSTRAINT suhuKey PRIMARY KEY (user_id, tanggal),
            FOREIGN KEY (user_id) REFERENCES t_akun(user_id)
        )
    """)

# Mengembalikan True jika terdapat entry pada t_suhu dengan user_id = id dan tanggal = date
# Mengembalikan False jika tidak terdapat
def isSuhuExist(id, date):
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    print(date)
    command = "SELECT user_id FROM t_suhu WHERE user_id = ? AND tanggal = ?"
    cursor.execute(command, (id, date.toString("yyyy-MM-dd")))
    rows = cursor.fetchall()
    return len(rows) > 0

# Mengembalikan riwayat user dengan user_id = id pada jangka waktu awal < tanggal < akhir
def getRiwayatSuhuTubuh(id, awal, akhir):
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT tanggal, suhu FROM t_suhu WHERE user_id = ? AND tanggal > ? AND tanggal <= ?"
    cursor.execute(command, (id, awal.toString("yyyy-MM-dd"), akhir.toString("yyyy-MM-dd")))
    rows = cursor.fetchall()

    test = getAllRiwayatSuhu(id)
    return rows

# Mengembalikan keseluruhan riwayat user dengan user_id = id
def getAllRiwayatSuhu(id):
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT tanggal, suhu FROM t_suhu WHERE user_id = ?"
    cursor.execute(command, (id,))
    rows = cursor.fetchall()
    return rows

# Menambahkan data suhu tubuh pada tabel t_suhu pada database
# Input id user, tanggal dicatatnya suhu, dan suhu dalam celcius
def addSuhuEntry(id, date, temp):
    if (isSuhuExist(id, date)): return False
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    suhu = (id, date.toString("yyyy-MM-dd"), temp)
    command = """INSERT INTO t_suhu(user_id, tanggal, suhu)
                VALUES (?, ?, ?)"""
    cursor.execute(command, suhu)
    cursor.connection.commit()
    return True

# Mengembalikan "Normal" jika suhu dievaluasi sehat
# Mengembalikan "Abnormal" jika suhu dievaluasi tidak sehat
def evaluasiSuhu(temp):
    t_norm = 37.8
    t_norm_b = 27.6
    if (temp > t_norm or temp < t_norm_b):
        return "Abnormal"
    else:
        return "Normal"


