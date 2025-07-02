from sqlalchemy import text
from sqlalchemy.orm import joinedload
from wtforms.validators import equal_to
from app.models import Question, QuestionRating, Choice, Survey, User
from tests.conftest import test_client, login_user_for_test, create_user_in_db
from app.extensions import db
from flask_login import current_user

def test_get_questions_auth(test_client, init_database):
    response = test_client.get('/api/questions')
    assert response.status_code != 200

def test_submit_survey(test_client, init_database, create_user_in_db):
    user = create_user_in_db('testuser', 'password123', email = "testusermail@mail.com", role='user')
    login_user_for_test(test_client, user)

    saved_survey = Survey.query.first()
    assert saved_survey is None #checks if db doesn't contain any other surveys - because it
                                # will take the first one
    data = [        # simulation of the data recived from frontend
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

    for idx, item in enumerate(data):
        choice = Choice(
            id=item["id"],
            question_id=idx + 1,
            answer_content=f"Sample answer {idx + 1}"
        )
        db.session.add(choice)

    db.session.flush()

    response = test_client.post('/api/submit-survey', json = data)
    print(response.get_json())
    assert response.status_code == 200
    assert response.get_json()['success'] == True

    saved_survey = Survey.query.options(joinedload(Survey.choices)).first()
    assert saved_survey is not None
    assert saved_survey.owner_id == User.query.filter_by(username = 'testuser').first().id
    assert len(saved_survey.choices) == 10

    # Cleanup at the end of test because data jumps to the other test
    Choice.query.delete()
    Question.query.delete()
    Survey.query.delete()
    db.session.commit()

def test_get_questions(test_client, init_database, create_user_in_db, questions_with_ratings):
    questions = questions_with_ratings['questions']
    #user = create_user_in_db('UserForTest', 'password123', email = 'testuseremail@mail.com', role = 'user')
    user = questions_with_ratings['user']
    login_user_for_test(test_client, user)

    response = test_client.get('/api/questions')

    data = response.get_json()
    print('data about to be printed -------------------------------')
    print(data)
    questions_received = [
    Question(
        id=q.get('id'),
        question_content=q['question_content'],
        question_type=q['question_type'],
        global_rating=q.get('global_rating', 0.0),
        choices=[Choice(answer_content=c['answer_content']) for c in q.get('choices', [])]
    ) for q in data
    ]

    num_of_one_question = 0 # to test if question is not returned multiple times
    if (q.question_content == 'High user rating 1' for q in questions_received):
        num_of_one_question += 1

    assert data is not None
    assert len(questions_received) == 10
    assert any(q.question_content == "High global rating 1" for q in questions_received)
    assert any(q.question_content == "Mood question" for q in questions_received)
    assert any(q.question_content == "High global rating 2" for q in questions_received)
    assert any(q.question_content == "High user rating 1" for q in questions_received)
    assert any(q.question_content == 'High user rating 2' for q in questions_received)
    assert any(q.question_content == 'High user rating 3' for q in questions_received)
    assert any(q.question_content == 'High user rating 4' for q in questions_received)
    assert any(q.question_content == 'High user rating 5' for q in questions_received)
    assert num_of_one_question == 1