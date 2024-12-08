def test_main_page_shows_up(test_client):
    """
    Проверить что на главной странице отображаются список ссылок
    """
    response = test_client.get("/")
    assert response.status_code == 200
    html_content = response.data.decode("utf-8")
    assert """<ul class="list-group">""" in html_content
