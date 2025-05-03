from sqlalchemy import text
from wtforms.validators import equal_to

from app.models import Question, QuestionRating, Choice
from tests.conftest import test_client, login_user_for_test
from app.extensions import db
from flask_login import current_user

def test_get_questions_auth(test_client, init_database):
    response = test_client.get('/api/questions')
    assert response.status_code != 200

def test_get_questions(test_client, init_database, create_user_in_db):
    user = create_user_in_db('UserForTest', 'password123', email = 'testuseremail@mail.com', role = 'user')
    login_user_for_test(test_client, user)

    questions = [
        # 6 questions with high user rating
        Question(
            question_content="High user rating 1",
            question_type="choice",
            global_rating=0.70,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 2",
            question_type="choice",
            global_rating=0.65,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 3",
            question_type="choice",
            global_rating=0.61,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 4",
            question_type="choice",
            global_rating=0.65,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 5",
            question_type="choice",
            global_rating=0.65,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 6",
            question_type="choice",
            global_rating=0.65,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        # 2 pytania z globalnym rankingiem
        Question(
            question_content="High global rating 7",
            question_type="choice",
            global_rating=0.95,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High global rating 8",
            question_type="choice",
            global_rating=0.90,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),

        # Wildcards
        Question(
            question_content="Wildcard 1",
            question_type="choice",
            global_rating=0.30,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="Wildcard 2",
            question_type="choice",
            global_rating=0.25,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="Wildcard 3",
            question_type="choice",
            global_rating=0.10,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="Wildcard 4",
            question_type="text",
            global_rating=0.05,
            choices=[]
        )
    ]

    db.session.bulk_save_objects(questions)
    db.session.commit()
    cur_user_id = user.id

    ratings = [
        QuestionRating(
            question_id=1,
            user_id=cur_user_id,
            rating=0.88
        ),
        QuestionRating(
            question_id=2,
            user_id=cur_user_id,
            rating=0.79
        ),
        QuestionRating(
            question_id=3,
            user_id=cur_user_id,
            rating=0.91
        ),
        QuestionRating(
            question_id=4,
            user_id=cur_user_id,
            rating=0.95
        ),
        QuestionRating(
            question_id=5,
            user_id=cur_user_id,
            rating=0.92
        ),
        QuestionRating(
            question_id=6,
            user_id=cur_user_id,
            rating=0.81
        ),
    ]

    db.session.bulk_save_objects(ratings)
    db.session.commit()

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
    assert any(q.question_content == 'High user rating 1' for q in questions_received)
    assert any(q.question_content == 'High user rating 2' for q in questions_received)
    assert any(q.question_content == 'High user rating 3' for q in questions_received)
    assert any(q.question_content == 'High user rating 4' for q in questions_received)
    assert any(q.question_content == 'High user rating 5' for q in questions_received)
    assert any(q.question_content == 'High user rating 6' for q in questions_received)
    assert num_of_one_question == 1
