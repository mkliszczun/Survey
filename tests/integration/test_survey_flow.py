from app.models import Survey, User, QuestionRating, Question
from tests.fixtures.users_fixtures import login_user_for_test
from tests.conftest import create_user_in_db

def test_survey_flow(test_client, questions_without_ratings, init_database, create_user_in_db):
    user = create_user_in_db('survey_flow_user', 'password', email = 'survey_flow@mail.com')
    bad_response = test_client.get('/survey') #to create app.context

    response = test_client.post('/api/login', json = {'email' : 'survey_flow@mail.com', 'password' : 'password'})

    assert response.status_code == 200
    assert response.get_json()['success'] is True

    response = test_client.get('/survey')
    assert b'js/survey.js' in response.data

    response = test_client.get('/api/questions')
    assert response.status_code == 200
    questions = response.get_json()
    assert len(questions) == 10

    data = [
        {"id": 2},
        {"id": 5},
        {"id": 9},
        {"id": 11},
        {"id": 19},
        {"id": 23},
        {"id": 26},
        {"id": 30},
        {"id": 35},
        {"id": 39}
    ]
    response = test_client.post('/api/submit-survey', json = data)

    assert response.status_code == 200

    user_id = User.query.filter_by(username = 'survey_flow_user').first().id
    survey = Survey.query.filter_by(owner_id = user_id).first()
    assert survey is not None

    ratings = QuestionRating.query.filter_by(user_id = user_id).all()
    assert ratings is not None

    global_rating = Question.query.filter_by(id = 1).first().global_rating
    assert global_rating is not None