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

con.execute("""
    INSERT INTO flights (route, departure_time, canceled, plane) VALUES (1,	'2024-10-02 10:00:00',	0,	2)
""")
flights = [
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
]
for route_id, passenger_id in flights:
    con.execute(f"""
        INSERT INTO passengers_has_flights VALUES ({route_id}, {passenger_id})
    """)

con.commit()
