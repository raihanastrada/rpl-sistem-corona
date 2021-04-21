import kasusHarian as kh

if __name__ == "__main__":
    try:
        kh.getLatestCase()
    except:
        kh.initializeDatabase()    
    kh.kasusHarian(True)