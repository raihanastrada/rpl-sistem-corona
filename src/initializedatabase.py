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

if __name__ == "__main__":
    initializeDatabase()