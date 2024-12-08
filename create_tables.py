import sqlite3


def create_tables(connection):
    with open("sqlite_script.txt", mode="r", encoding="utf8") as tables_statements:
        connection.executescript(tables_statements.read())
    connection.commit()


if __name__ == '__main__':
    connection = sqlite3.connect("airplanes.db")
    create_tables(connection)
