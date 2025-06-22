import flask_login
import pytest
from werkzeug.security import generate_password_hash
from app import db as _db
from app import User


@pytest.fixture(scope='function')
def create_user_in_db(init_database):

    created_users = []
    def _create_user(username, password, email, role='user'):
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user = User(username=username, password=hashed_password, email = email, role=role)
        _db.session.add(user)
        _db.session.commit()
        created_users.append(user)
        return user

    yield _create_user

def login_user_for_test(client, user):
    with client.session_transaction():
        flask_login.login_user(user)