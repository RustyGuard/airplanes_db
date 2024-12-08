import os
import sqlite3
from pathlib import Path

from flask import g

from database_connection import create_tables_if_not_exist, dict_factory

print(os.getcwd())
import pytest

from app import app
import main

TEST_DATABASE_PATH = "test_db.db"

@pytest.fixture()
def test_database_connection():
    connection = sqlite3.connect(TEST_DATABASE_PATH)
    create_tables_if_not_exist(connection)
    connection.row_factory = dict_factory
    yield connection
    Path(TEST_DATABASE_PATH).unlink()


@pytest.fixture()
def test_client(test_database_connection):
    with app.app_context():
        g._database = test_database_connection
        yield app.test_client()
        g._database = None
