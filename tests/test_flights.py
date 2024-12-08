import random

from tests.conftest import planes_with_pilots


def test_get_flight_page_without_flights(test_client):
    """
    Проверить что страница с вылетами открывается даже если не ссоздано ни одного полёта
    """
    response = test_client.get("/get_people_on_plane")
    assert response.status_code == 200
    html_content = response.data.decode("utf-8")
    assert "Люди на полете №" not in html_content


def test_create_flight(test_client, planes_with_pilots, routes):
    """
    Проверить что создание полёта выполняется
    """
    plane_id, pilot_id = random.choice(planes_with_pilots)
    route = random.choice(routes)
    response = test_client.post("/get_people_on_plane/add_flight", data={
        "departure_time": "2024-12-8 00:00",
        "route": route,
        "plane": plane_id,
    })
    assert response.status_code == 302
    response = test_client.get("/get_people_on_plane")
    assert response.status_code == 200
    html_content = response.data.decode("utf-8")
    assert "Люди на полете №" in html_content
