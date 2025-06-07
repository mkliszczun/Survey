import pytest


@pytest.fixture
def logged_user(create_user_in_db):
    create_user_in_db()