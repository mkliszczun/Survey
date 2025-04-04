from app import User
from app.extensions import db
from tests.conftest import login_user_for_test


def test_admin_dashboard_not_logged(test_client, init_database):
    response = test_client.get("/admin/")
    assert response.status_code == 403

def test_admin_dashboard_regular_user(test_client, init_database, create_user_in_db):
    user = create_user_in_db('testuser', 'password123', email = "testusermail@mail.com", role='user')
    login_user_for_test(test_client, user)

    response = test_client.get("/admin/")
    assert response.status_code == 403

def test_admin_dashboard_admin(test_client, init_database, create_user_in_db):
    admin = create_user_in_db('admin', 'password123', email = "testadminmail@mail.com", role = 'admin')
    login_user_for_test(test_client, admin)

    response = test_client.get("/admin/")
    assert response.status_code == 200