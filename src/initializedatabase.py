import loginQueries as lq
import rsQueries as rq
import kasusHarian as kh
import suhuQueries as sq

# Query menginisialisasi database
def initializeDatabase():
    lq.createCustomerDatabase()
    lq.createUserDatabase()
    rq.createPemesananDatabase()
    rq.createRSDatabase()
    kh.initTableKasus()
    sq.createSuhuDatabase()
    lq.addAdminEntry("Admin Noler", "adminnoler@gmail.com", "adminnoler", 87881528377)
    lq.addAdminEntry("Admin Aas", "adminaas@gmail.com", "adminaas", 811911777)
    lq.addAdminEntry("Admin Maxi", "adminmaxi@gmail.com", "adminmaxi", 812912778)
    lq.addAdminEntry("Admin Opal", "adminopal@gmail.com", "adminopal", 8119117778)
    lq.addAdminEntry("Admin Gobin", "admingobin@gmail.com", "admingobin", 811922787)
    rq.addRSEntry('Jakarta Hospital', 'Jl. Jend. Sudirman No. Kav 49')
    rq.addRSEntry('Rumah Sakit Jakarta', 'Jl. Garnisun No. 1 Karet Semanggi Setia Budi')
    rq.addRSEntry('Jakarta Islamic Hospital', 'Jl. Cemp. Putih Tengah I No. 1')
    rq.addRSEntry('Gatot Subroto', 'Jl. Abdul Rahman Saleh 24')
    rq.addRSEntry('Gatot Subroto', 'Jl. Abdul Rahman Saleh 24')
    rq.addRSEntry('Rumah Sakit Cikini', 'Jl. Raden Saleh Raya No.40')
    rq.addRSEntry('Abdi Waluyo Hospital', 'Jl. HOS. Cokroaminoto No.31-33')
    rq.addRSEntry('RS Bunda Jakarta', 'Jl. Teuku Cik Ditiro 1 No.11')
    rq.addRSEntry('Royal Taruma Hospital', 'Daan Mogot Rd Kedaung No.34')

if __name__ == "__main__":
    initializeDatabase()