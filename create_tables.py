import sqlite3
from pathlib import Path

Path("airplanes.db").unlink()

con = sqlite3.connect("airplanes.db")
with open("sqlite_script.txt", mode="r", encoding="utf8") as tables_statements:
    con.executescript(tables_statements.read())
con.commit()
