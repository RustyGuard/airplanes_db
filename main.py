from flask import Flask, render_template, abort, request

from app import app
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
    get_tenure_hours_sum,
    get_ticket_price_average,
    get_passengers_with_payments,
    get_pilots_to_flights_count,
    get_people_on_plane,
)


@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/get_passengers_with_info")
def get_passengers_with_info_page():
    return render_template("get_passengers_with_info.html", passengers_with_info=get_passengers_with_info())


@app.route("/get_routes_info")
def get_routes_info_page():
    return render_template("get_routes_info.html", routes_info=get_routes_info())


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


@app.route("/get_tenure_hours_sum")
def get_tenure_hours_sum_page():
    return render_template("get_tenure_hours_sum.html", tenure_hours_sum=get_tenure_hours_sum())


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
    flight_id = 1
    return render_template("get_people_on_plane.html", people_on_plane=get_people_on_plane(flight_id), flight_id=flight_id)


app.run(debug=True)
