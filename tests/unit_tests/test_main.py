def test_main_template_returning(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
