import sqlite3

# Membuat Tabel User jika belum ada, mengembalikan koneksi ke user database
def createUserDatabase():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS
                    user(user_id INTEGER PRIMARY KEY,
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
                    customer(user_id INTEGER PRIMARY KEY,
                    membership_status BOOLEAN NOT NULL DEFAULT 0,
                    PIN INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user(user_id)
        )""")
    return cursor

# Membuat Tabel Admin jika belum ada, mengembalikan koneksi ke admin database
def createAdminDatabase():
    return

# Mengecek jika email sudah terdapat pada database User, jika sudah terdapat dikembalikan True, jika tidak dikembalikan False
def isEmailExist(email):
    connectionUser = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connectionUser.cursor()
    command = "SELECT user_id FROM user WHERE user.email = ?"
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    return (len(rows) > 0)

# Menghitung banyak user pada database User
def userCount():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * from user")
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
    commandUser = """INSERT INTO user(name, email, password, role, number)
                    VALUES (?, ?, ?, ?, ?)"""
    cursorUser.execute(commandUser, user)
    count = userCount() # user count
    cursorUser.connection.commit()
    commandCustomer = """INSERT INTO customer(user_id, membership_status, PIN)
                        VALUES (?, ?, ?)"""
    customer = (count + 1, 0, uPIN)
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
    commandInsert = """INSERT INTO user(name, email, password, role, number) 
                    VALUES (?, ?, ?, ?, ?)"""
    cursor.execute(commandInsert, user)
    cursor.connection.commit()
    return True

# Menampilkan tabel user
def showUserEntries():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT * FROM user"
    cursor.execute(command)
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Table User Empty")
        return
    for row in rows:
        print(row)
    return

# Menampilkan tabel customer
def showCustomerEntries():
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = "SELECT * FROM customer"
    cursor.execute(command)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    return

# Mengambil pin dari customer, jika tidak ditemukan return False
def getPIN(email):
    if not isEmailExist(email): return False
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """SELECT customer.pin FROM user JOIN customer ON
                customer.user_id = user.user_id WHERE email = ?"""
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
    command = """SELECT password, role FROM user WHERE email = ?"""
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
    command = """SELECT customer.membership_status 
                FROM user join customer
                ON user.user_id = customer.user_id
                WHERE email = ?"""
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    if len(rows) == 0: return None
    return bool(rows[0][0])

# Mengambil nama user dengan input email
def getName(email):
    if not isEmailExist(email): return None
    connection = sqlite3.connect('sistem-tracking-corona.db')
    cursor = connection.cursor()
    command = """SELECT name FROM user WHERE email = ?"""
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    return rows[0][0]

if __name__ == "__main__":
    print("running loginQueries")
    createUserDatabase()
    createCustomerDatabase()
    addAdminEntry('Admin Noler', 'adminnoler@gmail.com', 'adminnoler', 87881528377)