from loginUI import startLogin as runApp
from initializedatabase import initializeDatabase as initDb

try:
    runApp()
except:
    initDb()
    runApp()