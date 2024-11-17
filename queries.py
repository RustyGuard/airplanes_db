import itertools

from database_connection import get_connection


# Запрос на выборку избранных полей таблицы, с использованием синонима
# (алиаса) и сортировкой записей (ORDER BY).
def get_passengers_with_info():
    return list(get_connection().execute("""
        SELECT id, name, address, phone_number 
        FROM passengers
        ORDER BY name;
    """))


# Запрос с использованием сортировки (ORDER BY) и группировки (GROUP BY).
def get_routes_info():
    return list(get_connection().execute("""
        SELECT 
        departure.airport_name as departure_airport_name, 
        destination.airport_name as destination_airport_name, 
        COUNT(flights.id) as flights_count FROM routes
        LEFT JOIN flights ON flights.route = routes.id
        JOIN airports departure ON departure_airport = departure.id
        JOIN airports destination ON destination_airport = destination.id
        GROUP BY routes.id
        ORDER BY departure.airport_name;
    """))


# Запрос с использованием предложения DISTINCT.
def get_flights_departure_times():
    return list(get_connection().execute("""
        SELECT DISTINCT departure_time FROM flights;
    """))


# Запрос с использованием операций сравнения.
def get_cheap_routes(max_price: int):
    return list(get_connection().execute(f"""
        SELECT * FROM routes
        WHERE ticket_price_rub <= {max_price};
    """))


# Запросы для предикатов: IN, BETWEEN, LIKE, IS NULL.

# 5.1
def get_destination_cities():
    """
    :return: Список городов прилёта
    """
    return list(get_connection().execute("""
        SELECT name FROM cities
        WHERE cities.id IN (SELECT airport_city FROM airports WHERE airport_city IN (SELECT destination_airport FROM routes));
    """))


# 5.2
def get_routes_within_duration_interval(min_duration: int = 60, max_duration: int = 300):
    return list(get_connection().execute(f"""
        SELECT departure.airport_name as departure_airport_name, destination.airport_name as destination_airport_name, flight_time_min FROM routes
        JOIN airports departure ON departure_airport = departure.id
        JOIN airports destination ON destination_airport = destination.id
        WHERE flight_time_min BETWEEN {min_duration} AND {max_duration};
    """))


# 5.3
def get_pilots_that_start_with(name_start: str = "Ива"):
    return list(get_connection().execute(f"""
        SELECT name FROM pilots
        WHERE name LIKE "{name_start}%";
    """))


# 5.4
def get_passengers_with_address():
    return list(get_connection().execute("""
        SELECT * FROM passengers
        WHERE address IS NULL;
    """))


# Запросы с использованием агрегатных функций (COUNT, SUM, AVG,
# MAX, MIN ), производящие обобщенную групповую обработку значений
# полей (используя ключевые фразы GROUP BY и HAVING).

# 6.1
def get_cities_to_airports_count():
    return list(get_connection().execute("""
        SELECT 
        COUNT(*) as count, 
        (select name from cities where cities.id = airport_city) as name,
        airport_city
        FROM airports
        GROUP BY airport_city
        ORDER BY count DESC;
    """))


# 6.2
def get_ticket_price_average(max_price: int):
    return list(get_connection().execute(f"""
        SELECT departure_airport, AVG(ticket_price_rub) as avg FROM routes
        GROUP BY departure_airport
        HAVING MAX(ticket_price_rub) < {max_price};
    """))


# Запрос на выборку данных из двух связанных таблиц. Выбрать несколько
# полей, по которым сортируется вывод.
def get_passengers_with_payments():
    """
    :return: Словарь от имени пассажира к суммам его билетов, отсортированных по дате
    """
    return {
        name: [price_tuple["ticket_price_rub"] for price_tuple in prices]
        for name, prices in
        itertools.groupby([
            entry
            for entry in get_connection().execute("""
                SELECT name, ticket_price_rub FROM passengers
                LEFT JOIN passengers_has_flights ON passengers_passport_id = passengers.id
                JOIN flights ON flights_flight_id = flights.id
                JOIN routes ON flights.route = routes.id
                ORDER BY name, departure_time
            """)
        ], key=lambda x: x["name"])
    }


# Многотабличный запрос с использованием внутреннего и внешнего
# соединения.
def get_pilots_to_flights_count():
    """
    :return: Словарь от пилота к количеству вылетов
    """
    # У пилота обязан быть самолёт
    # Однако мы хотим выводить пилотов, у которых ещё не было полётов
    return list(
        get_connection().execute("""
            SELECT name, count(flights.id) as flights_count FROM pilots
            JOIN planes ON pilots.id = planes.pilot
            LEFT JOIN flights ON flights.plane = planes.id
            GROUP BY name
        """)
    )


# Многотабличный запрос с использованием оператора UNION.
def get_people_on_plane(flight_id: int) -> list[str]:
    """
    :param flight_id: идентификатор полёта
    :return: Список людей, присутствующих на полёте
    """
    return list(
        get_connection().execute(f"""
            SELECT passengers.id as id, name, 'passenger' as type FROM passengers_has_flights 
            JOIN passengers ON passengers.id = passengers_has_flights.passengers_passport_id
            WHERE passengers_has_flights.flights_flight_id = {flight_id}
            UNION
            SELECT pilots.id as id, name, 'pilot' as type FROM flights
            JOIN planes ON flights.plane = planes.id
            JOIN pilots ON planes.pilot = pilots.id
            WHERE flights.id = {flight_id}
            ORDER BY name
        """)
    )
