import csv
import sqlite3

con = sqlite3.connect("airplanes.db")
plane_models = [
    "Боинг-747",
    "Ту-134",
    "Ил-62",
]
for entry in plane_models:
    con.execute(f"""INSERT INTO plane_models (model_name) VALUES ("{entry}")""")
    model_id, = next(con.execute(f"""SELECT plane_model_id FROM plane_models WHERE model_name = "{entry}" """))
    print(model_id)
    con.execute(
        f"""INSERT INTO planes (plane_model, manufacture_date, service_life, pilot) VALUES ({model_id}, date('now'), 0, 1)""")

with open('ISO3166.csv', mode="r", encoding="utf8") as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for country in spamreader:
        con.execute(f"""INSERT INTO countries (country_id, name) VALUES ("{country['Code']}", "{country['Name']}")""")
cities = set()
with open('airport-codes.csv', mode="r", encoding="utf8") as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for line in spamreader:
        if line["iata_code"] == "":
            continue
        print(line)
        if line['municipality'] not in cities:
            cities.add(line['municipality'])
            con.execute(f"""INSERT INTO cities (name, country) VALUES ("{line['municipality']}", "{line['iso_country']}")""")
        city_id, = next(con.execute(f"""SELECT city_id FROM cities WHERE name = "{line['municipality']}" """))
        print(f"{city_id=}")
        con.execute(f"""INSERT INTO airports (airport_name, airport_city) VALUES (?, ?)""", (line['name'], city_id))

con.commit()
