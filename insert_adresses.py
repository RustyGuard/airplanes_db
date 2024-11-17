import csv
import sqlite3

con = sqlite3.connect("airplanes.db")
con.execute(f"""DELETE FROM airports WHERE airport_city = 79;""")
# con.execute(f"""UPDATE passengers SET address = CONCAT("Улица Огарёва", " ", cast(ABS(FLOOR(RANDOM() % 1000)) as text) );""")
con.commit()