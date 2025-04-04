import pytest
from app.models import User
from werkzeug.security import check_password_hash

def test_user_registration(test_client, init_database): #test registering method
    response = test_client.post("/api/register", json = {
        "username" : "testuser",
        "password" : "testpassword",
        "email" : "testmail@test.com"
    })

    assert response.status_code == 200
    assert User.query.filter_by(email= "testmail@test.com").first()

def test_valid_registration(test_client): #test field registration
    response = test_client.post("/api/register", json = {
        "user" : "testuser"
    })

    assert response.status_code == 400

def test_valid_registration_taken_check(test_client, init_database): #test whether api checks if user is taken
    test_client.post("/api/register", json = {
        "username" : "testuser",
        "password" : "testpassword",
        "email" : "testmail@test.com"
    })

    response = test_client.post("/api/register", json = {
        "username" : "testuser",
        "password" : "testpassword",
        "email" : "testmail@test.com"
    })

    assert response.status_code == 409
