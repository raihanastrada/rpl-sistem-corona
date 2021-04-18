import sqlite3

# Membuat Tabel User jika belum ada, mengembalikan koneksi ke user database
def createUserDatabase():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS
                    t_akun(user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    number INT NOT NULL
        )""")
    return cursor

# Membuat Tabel Customer jika belum ada, mengembalikan koneksi ke customer database
def createCustomerDatabase():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS
                    t_customer(user_id INTEGER PRIMARY KEY,
                    membership_status DATE NOT NULL DEFAULT CURRENT_DATE,
                    PIN INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES t_akun(user_id)
        )""")
    return cursor

# Membuat Tabel Admin jika belum ada, mengembalikan koneksi ke admin database
def createAdminDatabase():
    return

# Mengecek jika email sudah terdapat pada database User, jika sudah terdapat dikembalikan True, jika tidak dikembalikan False
def isEmailExist(email):
    connectionUser = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connectionUser.cursor()
    command = "SELECT user_id FROM t_akun WHERE t_akun.email = ?"
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    return (len(rows) > 0)

# Menghitung banyak user pada database User
def userCount():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * from t_akun")
    return len(cursor.fetchall())

# Menambahkan Entry pada User Database dan Customer Database, membership status default = False
# PIN length = 6, dicek sebelum menggunakan fungsi
def addCustomerEntry(name, email, password, number, uPIN):
    if (isEmailExist(email)): return False
    connectionUser = sqlite3.connect('sistem-tracking-corona.db')
    cursorUser = connectionUser.cursor()
    connectionCustomer = sqlite3.connect('sistem-tracking-corona.db')
    cursorCustomer = connectionCustomer.cursor()
    user = (name, email, password, 'Customer', number)
    commandUser = """INSERT INTO t_akun(name, email, password, role, number)
                    VALUES (?, ?, ?, ?, ?)"""
    cursorUser.execute(commandUser, user)
    count = userCount() # user count
    cursorUser.connection.commit()
    commandCustomer = """INSERT INTO t_customer(user_id, PIN)
                        VALUES (?, ?)"""
    customer = (count + 1, uPIN)
    cursorCustomer.execute(commandCustomer, customer)
    cursorCustomer.connection.commit()
    return True

# Menambahkan User Entry pada User database dengan Role = "Admin" jika belum terdapat email yang sama pada Database
def addAdminEntry(name, email, password, number):
    if (isEmailExist(email)): # Tidak menambahkan entry jika sudah terdapat user dengan email yang sama
        return False
    connectionAdmin = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connectionAdmin.cursor()
    user = (name, email, password, 'Admin', number)
    commandInsert = """INSERT INTO t_akun(name, email, password, role, number) 
                    VALUES (?, ?, ?, ?, ?)"""
    cursor.execute(commandInsert, user)
    cursor.connection.commit()
    return True

# Menampilkan tabel user
def showUserEntries():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT * FROM t_akun"
    cursor.execute(command)
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Table t_akun Empty")
        return
    for row in rows:
        print(row)
    return

# Menampilkan tabel customer
def showCustomerEntries():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT * FROM t_customer"
    cursor.execute(command)
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Table t_customer Empty")
        return
    for row in rows:
        print(row)
    return

# Mengambil pin dari customer, jika tidak ditemukan return False
def getPIN(email):
    if not isEmailExist(email): return False
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """SELECT t_customer.pin FROM t_akun JOIN t_customer ON
                t_customer.user_id = t_akun.user_id WHERE email = ?"""
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    if len(rows) == 0: return False
    return rows[0][0]

# Mendapatkan info yang digunakan untuk login (password dan role) [0] == password, [1] == role
# Mengembalikan False jika user belum terdaftar
def getLoginInfo(email):
    if not isEmailExist(email): return False # Mengembalikan False jika user belum terdaftar
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """SELECT password, role FROM t_akun WHERE email = ?"""
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    return rows[0] # Mengembalikan password dan role user

# Mengembalikan status membership dari user
# Mengembalikan False jika belum menjadi member, True jika sudah menjadi member
# Mengembalikan None jika merupakan Admin, atau tidak terdaftar sebagai user
def getMembershipStatus(email):
    if not isEmailExist(email): return None
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """SELECT t_customer.membership_status > CURRENT_DATE,
                t_customer.membership_status
                FROM t_akun join t_customer
                ON t_akun.user_id = t_customer.user_id
                WHERE email = ?"""
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    if len(rows) == 0: return None
    return bool(rows[0][0]), rows[0][1]

# Mengambil nama user dengan input email
def getName(email):
    if not isEmailExist(email): return None
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """SELECT name FROM t_akun WHERE email = ?"""
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    return rows[0][0]

if __name__ == "__main__":
    print("running loginQueries")
    createUserDatabase()
    createCustomerDatabase()
    addAdminEntry('Admin Noler', 'adminnoler@gmail.com', 'adminnoler', 87881528377)
    addCustomerEntry('Noler Customer', 'nolercustomer@gmail.com', 'nolercustomer', 87881528378, 2486)
    print(getMembershipStatus('nolercustomer@gmail.com'))