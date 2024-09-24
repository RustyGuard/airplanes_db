import sqlite3
con = sqlite3.connect("airplanes.db")
print(list(con.execute("""SELECT * FROM planes""")))
