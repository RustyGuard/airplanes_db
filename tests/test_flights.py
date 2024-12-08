def test_get_flight_page_without_flights(test_client):
    response = test_client.get("/get_people_on_plane")
    assert response.status_code == 200
    html_content = response.data.decode("utf-8")
    assert "Люди на полете №" not in html_content
