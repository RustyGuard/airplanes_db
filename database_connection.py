import sqlite3
from sqlite3 import Error
from flask import g

from app import app
from create_tables import create_tables

DATABASE_PATH = "airplanes.db"


def create_tables_if_not_exist(connection):
    try:
        create_tables(connection)
    except Error as e:
        print(e)
        raise


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_connection():
    connection = getattr(g, '_database', None)
    if connection is None:
        connection = sqlite3.connect(DATABASE_PATH)
        create_tables_if_not_exist(connection)
        connection.row_factory = dict_factory
        g._database = connection
    return connection


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()