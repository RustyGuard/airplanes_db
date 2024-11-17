import datetime

import dateutil
from flask import render_template, request, redirect, url_for

from app import app
from database_connection import get_connection
from queries import (
    get_passengers_with_info,
    get_routes_info,
    get_flights_departure_times,
    get_cheap_routes,
    get_destination_cities,
    get_routes_within_duration_interval,
    get_pilots_that_start_with,
    get_passengers_with_address,
    get_cities_to_airports_count,
    get_ticket_price_average,
    get_passengers_with_payments,
    get_pilots_to_flights_count,
    get_people_on_plane,
)
from dateutil.parser import parse

@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/get_passengers_with_info")
def get_passengers_with_info_page():
    return render_template("get_passengers_with_info.html", passengers_with_info=get_passengers_with_info())


@app.route("/get_passengers_with_info/update", methods=["POST"])
def set_passengers_with_info_page():
    connection = get_connection()
    connection.execute("""
        UPDATE passengers 
        SET name=?, address=?, phone_number=? 
        WHERE id = ?;
    """, (request.form["name"], request.form["address"] or None, request.form["phone_number"] or None, request.form["id"]))
    connection.commit()
    return redirect(url_for("get_passengers_with_info_page"))


@app.route("/get_passengers_with_info/insert", methods=["POST"])
def insert_passengers_with_info_page():
    connection = get_connection()
    connection.execute("""
        INSERT INTO passengers (name, address, phone_number)
        VALUES (?, ?, ?);
    """, (request.form["name"], request.form["address"] or None, request.form["phone_number"] or None))
    connection.commit()
    return redirect(url_for("get_passengers_with_info_page"))


@app.route("/get_passengers_with_info/delete")
def delete_passengers_with_info_page():
    connection = get_connection()
    connection.execute("""
        DELETE FROM passengers
        WHERE id = ?;
    """, (request.args["id"],))
    connection.commit()
    return redirect(url_for("get_passengers_with_info_page"))


@app.route("/get_routes_info")
def get_routes_info_page():
    airports = list(get_connection().execute("""
        SELECT 
        airports.id as id, 
        airport_name, 
        cities.name as city_name, 
        countries.name as country_name 
        FROM airports
        JOIN cities ON airports.airport_city = cities.id
        JOIN countries ON cities.country = countries.id 
        ORDER BY country_name, city_name, airport_name
    """))

    return render_template("get_routes_info.html", routes_info=get_routes_info(),
                           airports=airports)


@app.route("/get_routes_info/add", methods=["POST"])
def add_routes_info_page():
    connection = get_connection()
    connection.execute("""
        INSERT INTO routes (
        departure_airport,
        destination_airport,
        ticket_price_rub,
        flight_time_min
        )
        VALUES (?, ?, ?, ?);
    """, (
        request.form["departure_airport"],
        request.form["destination_airport"],
        request.form["ticket_price_rub"],
        request.form["flight_time_min"],
    ))
    connection.commit()
    return redirect(url_for("get_routes_info_page"))


@app.route("/get_flights_departure_times")
def get_flights_departure_times_page():
    return render_template("get_flights_departure_times.html", flights_departure_times=get_flights_departure_times())


@app.route("/get_cheap_routes")
def get_cheap_routes_page():
    max_price = 5000
    return render_template("get_cheap_routes.html", cheap_routes=get_cheap_routes(max_price), max_price=max_price)


@app.route("/get_destination_cities")
def get_destination_cities_page():
    return render_template("get_destination_cities.html", destination_cities=get_destination_cities())


@app.route("/get_routes_within_duration_interval")
def get_routes_within_duration_interval_page():
    max_duration = 60
    min_duration = 30
    return render_template("get_routes_within_duration_interval.html",
                           routes_within_duration_interval=get_routes_within_duration_interval(min_duration=min_duration, max_duration=max_duration),
                           min_duration=min_duration, max_duration=max_duration)


@app.route("/get_pilots_that_start_with")
def get_pilots_that_start_with_page():
    starts_with = "А"
    return render_template("get_pilots_that_start_with.html", pilots_that_start_with=get_pilots_that_start_with(starts_with), starts_with=starts_with)


@app.route("/get_passengers_with_address")
def get_passengers_with_address_page():
    return render_template("get_passengers_with_address.html", passengers_with_address=get_passengers_with_address())


@app.route("/get_cities_to_airports_count")
def get_cities_to_airports_count_page():
    return render_template("get_cities_to_airports_count.html", cities_to_airports_count=get_cities_to_airports_count())


@app.route("/get_ticket_price_average")
def get_ticket_price_average_page():
    max_price = 30000
    return render_template("get_ticket_price_average.html", ticket_price_average=get_ticket_price_average(max_price), max_price=max_price)


@app.route("/get_passengers_with_payments")
def get_passengers_with_payments_page():
    return render_template("get_passengers_with_payments.html", passengers_with_payments=get_passengers_with_payments())


@app.route("/get_pilots_to_flights_count")
def get_pilots_to_flights_count_page():
    return render_template("get_pilots_to_flights_count.html", pilots_to_flights_count=get_pilots_to_flights_count())


@app.route("/get_people_on_plane")
def get_people_on_plane_page():
    flight_id = request.args.get("flight_id", 1)
    flights_ids = get_connection().execute("""SELECT id FROM flights""")
    passengers = list(get_connection().execute(f"""
        SELECT id, name FROM passengers
        EXCEPT 
        SELECT id, name FROM passengers_has_flights 
            JOIN passengers ON passengers.id = passengers_has_flights.passengers_passport_id
            WHERE passengers_has_flights.flights_flight_id = ?
    """, (flight_id,)))
    planes = list(get_connection().execute("""
        SELECT planes.id as id, model_name, pilots.name as pilot_name FROM planes
        JOIN plane_models ON planes.plane_model = plane_models.id       
        JOIN pilots ON planes.pilot = pilots.id 
    """))
    routes = list(get_connection().execute("""
        SELECT 
        routes.id as id,
        departure.airport_name as departure_airport_name, 
        destination.airport_name as destination_airport_name
        FROM routes
        JOIN airports departure ON departure_airport = departure.id
        JOIN airports destination ON destination_airport = destination.id
    """))
    return render_template("get_people_on_plane.html",
                           people_on_plane=get_people_on_plane(flight_id),
                           flight_id=flight_id,
                           flights_ids=flights_ids,
                           passengers=passengers,
                           planes=planes,
                           routes=routes)


@app.route("/get_people_on_plane/insert", methods=["POST"])
def add_people_on_plane_page():
    flight_id = request.args.get("flight_id", 1)
    connection = get_connection()
    connection.execute(f"""
        INSERT INTO passengers_has_flights (passengers_passport_id, flights_flight_id)
        VALUES (?, ?) 
    """, (request.form["passenger_id"], flight_id))
    connection.commit()
    return redirect(url_for("get_people_on_plane_page", flight_id=request.args["flight_id"]))


@app.route("/get_people_on_plane/delete", methods=["GET"])
def remove_people_on_plane_page():
    connection = get_connection()
    connection.execute(f"""
        DELETE FROM passengers_has_flights 
        WHERE passengers_passport_id=? and flights_flight_id=?
    """, (request.args["passenger_id"], request.args["flight_id"]))
    print(request.args)
    connection.commit()
    return redirect(url_for("get_people_on_plane_page", flight_id=request.args["flight_id"]))

@app.route("/get_people_on_plane/add_flight", methods=["POST"])
def add_flight():
    print(request.form)
    departure_time = parse(request.form["departure_time"])
    print(departure_time)
    connection = get_connection()
    result = next(connection.execute(f"""
        INSERT INTO flights 
        (route, departure_time, plane)
        VALUES (?, ?, ?)
        RETURNING id
    """, (request.form["route"], departure_time, request.form["plane"])))
    connection.commit()
    return redirect(url_for("get_people_on_plane_page", flight_id=result["id"]))


app.run(debug=True)
