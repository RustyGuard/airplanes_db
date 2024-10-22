import csv
import sqlite3

con = sqlite3.connect("airplanes.db")
plane_models_with_pilots = [
    ("Боинг-747", "Головин Артём"),
    ("Ту-134", "Черепанов Артемий"),
    ("Ил-62", "Михаил Макарьевич"),
]
for (model_name, pilot_name) in plane_models_with_pilots:
    con.execute(f"""INSERT INTO plane_models (model_name) VALUES ("{model_name}")""")
    model_id, = next(con.execute(f"""SELECT id FROM plane_models WHERE model_name = "{model_name}" """))
    print(model_id)
    con.execute(
        f"""INSERT INTO planes (plane_model, manufacture_date, service_life, pilot) 
        VALUES ({model_id}, date('now'), 0, 1)"""
    )
    plane_id, = next(con.execute(f"""SELECT id FROM planes WHERE plane_model = "{model_id}" """))
    con.execute(f"""
        INSERT INTO pilots (
            name,
            address,
            phone_number
        ) VALUES (
            '{pilot_name}', null, null
        )
    """)
    pilot_id, = next(con.execute(f"""SELECT id FROM pilots WHERE name = "{pilot_name}" """))
    con.execute(f"""
        UPDATE planes SET pilot = {pilot_id} WHERE id = {plane_id}
    """)

with open('ISO3166.csv', mode="r", encoding="utf8") as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for country in spamreader:
        con.execute(f"""INSERT INTO countries (id, name) VALUES ("{country['Code']}", "{country['Name']}")""")
cities = set()
with open('airport-codes.csv', mode="r", encoding="utf8") as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    for line in spamreader:
        if line["iata_code"] == "":
            continue
        print(line)
        if line['municipality'] not in cities:
            cities.add(line['municipality'])
            con.execute(
                f"""INSERT INTO cities (name, country) VALUES ("{line['municipality']}", "{line['iso_country']}")""")
        city_id, = next(con.execute(f"""SELECT id FROM cities WHERE name = "{line['municipality']}" """))
        print(f"{city_id=}")
        con.execute(f"""INSERT INTO airports (airport_name, airport_city) VALUES (?, ?)""", (line['name'], city_id))

routes = [
    (7367, 1418, 4200, 69),
    (1418, 7367, 6900, 42),
]
for departure_airport, destination_airport, ticket_price_rub, flight_time_min in routes:
    con.execute(f"""
        INSERT INTO routes (departure_airport, destination_airport, ticket_price_rub, flight_time_min) VALUES
        ({departure_airport}, {destination_airport}, {ticket_price_rub}, {flight_time_min})
    """)

passengers = [
    "Вдовенко Ксения Григорьевна",
    "Вяльцев Алексей Максимович",
    "Грумеза Румяна Александровна",
    "Гусева Мария Олеговна",
    "Замулин Арсений Дмитриевич",
    "Зотова Арина Игоревна",
    "Кирясова Зоя Александровна",
    "Мельниченко Ирина Юрьевна",
    "Мотяков Денис Дмитриевич",
    "Никулин Иван Александрович",
    "Петровский Леонид Алексеевич",
    "Провоторов Никита Сергеевич",
    "Свиридов Кирилл Александрович",
    "Смирнов Виктор Сергеевич",
    "Телегин Андрей Витальевич",
    "Цуканов Егор Владимирович",
    "Александров Роман Алексеевич",
    "Бигильдин Вячеслав Андреевич",
    "Головин Артём Александрович",
    "Добина Алина Дмитриевна",
    "Добрышкина Полина Александровна",
    "Загородний Александр",
    "Заикина Юлия Сергеевна",
    "Козлов Анатолий Романович",
    "Куприянов Роман Валерьевич",
    "Манаинков Лев Андреевич",
    "Рязанцев Даниил Валерьевич",
    "Соколова Алёна Дмитриевна",
    "Тамбовцев Александр Сергеевич",
    "Таранец Максим Евгеньевич",
    "Фриз Максим Евгеньевич",
    "Черепанов Артемий Юрьевич",
]
for passenger_name in passengers:
    con.execute(f"""
        INSERT INTO passengers (name, address, phone_number) VALUES ('{passenger_name}', null, null)
    """)

FLIGHTS_COUNT = 30
for i in range(FLIGHTS_COUNT):
    con.execute("""
        INSERT INTO flights (route, departure_time, canceled, plane) VALUES ((SELECT id FROM routes ORDER BY RANDOM() LIMIT 1), 
        datetime(strftime('%s', '2024-10-01 00:00:00') +
                abs(RANDOM() % (strftime('%s', '2024-10-31 23:59:59') -
                                strftime('%s', '2024-10-01 00:00:00'))
                   ),
                'unixepoch'), 0, (SELECT id FROM planes ORDER BY RANDOM() LIMIT 1))
    """)
PASSENGERS_PER_FLIGHT = 5
for i in range(FLIGHTS_COUNT * PASSENGERS_PER_FLIGHT):
    con.execute("""
        INSERT OR IGNORE INTO passengers_has_flights (passengers_passport_id, flights_flight_id) VALUES (
            (SELECT id FROM passengers ORDER BY RANDOM() LIMIT 1),
            (SELECT id FROM flights ORDER BY RANDOM() LIMIT 1)
        )
    """)

con.commit()
