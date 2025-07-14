import flask_login
import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from app.config import TestConfig
from app.models import db as _db
from app.models import User
from fixtures.question_fixtures import questions_without_ratings,questions_with_ratings, questions_with_global_ratings
from fixtures.survey_fixtures import survey_data_for_one_question_with_big_score_diff
from fixtures.users_fixtures import create_user_in_db,login_user_for_test

@pytest.fixture(scope='module') #creates app and initiates db. Done this way to avoid app context issues
def test_client():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        with app.test_client() as client:
            _db.create_all()
            yield client
            _db.drop_all()


@pytest.fixture(scope='function') #mock db transactions - rolled back after each function test
def init_database(test_client):
    _db.session.begin_nested()
    yield
    _db.session.rollback()
    _db.session.remove()
