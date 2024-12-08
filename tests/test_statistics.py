import pytest

statistics_pages = [
    "/get_flights_departure_times",
    "/get_cheap_routes",
    "/get_destination_cities",
    "/get_routes_within_duration_interval",
    "/get_pilots_that_start_with",
    "/get_passengers_with_address",
    "/get_cities_to_airports_count",
    "/get_ticket_price_average",
    "/get_passengers_with_payments",
    "/get_pilots_to_flights_count",
]


@pytest.mark.parametrize(
    "page_url",
    statistics_pages,
)
def test_get_statistics_page(test_client, page_url: str):
    """
    Проверить что страницы со статистикой отображаются даже с пустой бд
    """
    response = test_client.get(page_url)
    assert response.status_code == 200
