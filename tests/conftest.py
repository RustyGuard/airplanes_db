import csv
import os
import random
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


@pytest.fixture()
def planes_with_pilots(test_database_connection) -> list[tuple[str, str]]:
    con = test_database_connection
    plane_models_with_pilots = [
        ("Боинг-747", "Головин Артём"),
        ("Ту-134", "Черепанов Артемий"),
        ("Ил-62", "Михаил Макарьевич"),
    ]
    planes_with_pilots = []
    for (model_name, pilot_name) in plane_models_with_pilots:
        model_id = next(con.execute(f"""INSERT INTO plane_models (model_name) VALUES ("{model_name}") RETURNING id"""))[
            "id"]
        plane_id = next(con.execute(
            f"""INSERT INTO planes (plane_model, manufacture_date, service_life, pilot) 
            VALUES ({model_id}, date('now'), 0, 1) RETURNING id"""
        ))["id"]
        pilot_id = next(con.execute(f"""
            INSERT INTO pilots (
                name,
                address,
                phone_number
            ) VALUES (
                '{pilot_name}', null, null
            )
            RETURNING id
        """))["id"]
        con.execute(f"""
            UPDATE planes SET pilot = {pilot_id} WHERE id = {plane_id}
        """)
        planes_with_pilots.append((plane_id, pilot_id))
    con.commit()
    return planes_with_pilots


@pytest.fixture()
def countries(test_database_connection):
    con = test_database_connection
    with open('ISO3166.csv', mode="r", encoding="utf8") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for country in spamreader:
            con.execute(f"""INSERT INTO countries (id, name) VALUES ("{country['Code']}", "{country['Name']}")""")


@pytest.fixture()
def airports(test_database_connection, countries) -> list[str]:
    con = test_database_connection
    cities = set()
    airports = []
    with open('airport-codes.csv', mode="r", encoding="utf8") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for line in spamreader:
            if line["iata_code"] == "":
                continue
            if line['municipality'] not in cities:
                cities.add(line['municipality'])
                con.execute(
                    f"""INSERT INTO cities (name, country) VALUES ("{line['municipality']}", "{line['iso_country']}")""")
            city_id, = next(con.execute(f"""SELECT id FROM cities WHERE name = "{line['municipality']}" """))
            airport_id = next(
                con.execute(f"""INSERT INTO airports (airport_name, airport_city) VALUES (?, ?) RETURNING id""",
                            (line['name'], city_id)))["id"]
            airports.append(airport_id)
    return airports


@pytest.fixture()
def routes(test_database_connection, airports) -> list[str]:
    con = test_database_connection
    routes_count = 5
    routes = []
    for i in range(routes_count):
        departure_airport = random.choice(airports)
        destination_airport = random.choice(airports)
        ticket_price_rub = random.randint(200, 2000)
        flight_time_min = random.randint(60, 600)
        route_id = next(con.execute(f"""
            INSERT INTO routes (departure_airport, destination_airport, ticket_price_rub, flight_time_min) VALUES
            ({departure_airport}, {destination_airport}, {ticket_price_rub}, {flight_time_min})
            RETURNING id
        """))["id"]
        routes.append(route_id)
    return routes
