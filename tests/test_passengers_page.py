from bs4 import BeautifulSoup


def test_get_passengers(test_client):
    """
    Проверить что страница отображения пассажиров отображается даже без созданных пассажиров
    """
    response = test_client.get("/get_passengers_with_info")
    assert response.status_code == 200
    html_content = response.data.decode("utf-8")
    assert "<h1>Все пассажиры с информацией</h1>" in html_content


def test_create_passenger(test_client):
    """
    Проверить что создание пассажира выполняется.
    Проверить что созданный пассажир появляется на страничке
    """
    response = test_client.post("/get_passengers_with_info/insert", data={
        "name": "test_name",
        "address": "test_address",
        "phone_number": "test_phone",
    })
    assert response.status_code == 302
    passengers = get_passengers_in_table(test_client)
    assert passengers == [
        [
            "test_name",
            "test_address",
            "test_phone",
        ]
    ]


def get_first_passenger_id(test_client) -> str:
    """
    Вернуть первый попавшийся на странице passenger_id
    """
    get_response = test_client.get("/get_passengers_with_info")
    assert get_response.status_code == 200
    html_content = get_response.data.decode("utf-8")
    soup = BeautifulSoup(html_content, 'html.parser')
    passenger_id = soup.find(id="exampleModal1").input.get("value")
    return passenger_id


def get_passengers_in_table(test_client) -> list[list[str]]:
    """
    Вернуть пассажиров, отображаемых в таблице
    """
    get_response = test_client.get("/get_passengers_with_info")
    assert get_response.status_code == 200
    html_content = get_response.data.decode("utf-8")
    soup = BeautifulSoup(html_content, 'html.parser')
    passenger_table = soup.table.tbody
    return [
        [column.string for column in row.find_all("td")[:3]]
        for row in passenger_table.find_all("tr")
    ]


def test_update_passenger(test_client):
    """
    Проверить что обновление пассажиров выполняется и изменяет данные в таблице
    """
    insert_response = test_client.post("/get_passengers_with_info/insert", data={
        "name": "test_name",
        "address": "test_address",
        "phone_number": "test_phone",
    })
    assert insert_response.status_code == 302
    passenger_id = get_first_passenger_id(test_client)
    response = test_client.post("/get_passengers_with_info/update", data={
        "id": passenger_id,
        "name": "new_test_name",
        "address": "new_test_address",
        "phone_number": "new_test_phone",
    })
    assert response.status_code == 302
    passengers = get_passengers_in_table(test_client)
    assert passengers == [
        [
            "new_test_name",
            "new_test_address",
            "new_test_phone",
        ]
    ]


def test_delete_passenger(test_client):
    """
    Проверить что удаление пассажира удаляет запись в таблице
    """
    insert_response = test_client.post("/get_passengers_with_info/insert", data={
        "name": "test_name",
        "address": "test_address",
        "phone_number": "test_phone",
    })
    assert insert_response.status_code == 302
    passenger_id = get_first_passenger_id(test_client)
    response = test_client.get("/get_passengers_with_info/delete", query_string={
        "id": passenger_id,
    })
    assert response.status_code == 302
    passengers = get_passengers_in_table(test_client)
    assert len(passengers) == 0
