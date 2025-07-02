import pytest
from sqlalchemy import delete

from app.models import Question, Choice, QuestionRating, db as _db

@pytest.fixture(scope='function')
def questions_without_ratings(init_database):

    #clean not to create conflict with id = 2
    # _db.session.query(Choice).delete()
    # _db.session.query(Question).delete()
    _db.session.execute(delete(Choice))
    _db.session.execute(delete(Question))
    _db.session.commit()

    _db.session.expire_all()

    questions = [
        # 6 questions with high user rating
        Question(
            question_content="High user rating 1",
            question_type="choice",
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            id = 2,
            question_content="Mood question",
            question_type="choice",
            choices=[
                Choice(answer_content="1"),
                Choice(answer_content="2"),
                Choice(answer_content="3"),
                Choice(answer_content="4"),
                Choice(answer_content="5"),
                Choice(answer_content="6"),
                Choice(answer_content="7"),
                Choice(answer_content="8"),
                Choice(answer_content="9"),
                Choice(answer_content="10")
            ]
        ),
        Question(
            question_content="High user rating 3",
            question_type="choice",
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 4",
            question_type="choice",
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 5",
            question_type="choice",
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 6",
            question_type="choice",
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
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High global rating 8",
            question_type="choice",
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
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="Wildcard 2",
            question_type="choice",
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="Wildcard 3",
            question_type="choice",
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="Wildcard 4",
            question_type="text",
            choices=[]
        )
    ]

    _db.session.add_all(questions)
    _db.session.commit()

    yield {
        'questions' : questions,
    }

    _db.session.close()

@pytest.fixture(scope='function')
def questions_with_global_ratings(init_database):


    #clean not to create conflict with id = 2
    _db.session.query(Choice).delete()
    _db.session.query(Question).delete()
    _db.session.commit()

    _db.session.expire_all()

    questions = [
        # 6 questions with high user rating
        Question(
            question_content="High global rating 1",
            question_type="choice",
            global_rating=7,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            id=2,
            question_content="Mood question",
            question_type="choice",
            global_rating=1,
            choices=[
                Choice(answer_content="1"),
                Choice(answer_content="2"),
                Choice(answer_content="3"),
                Choice(answer_content="4"),
                Choice(answer_content="5"),
                Choice(answer_content="6"),
                Choice(answer_content="7"),
                Choice(answer_content="8"),
                Choice(answer_content="9"),
                Choice(answer_content="10")
            ]
        ),
        Question(
            question_content="High global rating 2",
            question_type="choice",
            global_rating=6,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),

        Question(
            question_content="High user rating 1",
            question_type="choice",
            global_rating=6,
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
            global_rating=0.65,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 4",
            question_type="choice",
            global_rating=0.95,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
        Question(
            question_content="High user rating 5",
            question_type="choice",
            global_rating=0.90,
            choices=[
                Choice(answer_content="A"),
                Choice(answer_content="B"),
                Choice(answer_content="C")
            ]
        ),
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
        )
    ]

    _db.session.add_all(questions)
    _db.session.commit()

    return questions

@pytest.fixture(scope='function')
def questions_with_ratings(questions_with_global_ratings, create_user_in_db):

    _db.session.query(Choice).delete()
    #_db.session.query(Question).delete()
    _db.session.query(QuestionRating).delete()
    _db.session.commit()

    _db.session.expire_all()

    questions = questions_with_global_ratings
    high_user_rat_question_1 = next((q for q in questions if q.question_content == "High user rating 1"), None)
    high_user_rat_question_2 = next((q for q in questions if q.question_content == "High user rating 2"), None)
    high_user_rat_question_3 = next((q for q in questions if q.question_content == "High user rating 3"), None)
    high_user_rat_question_4 = next((q for q in questions if q.question_content == "High user rating 4"), None)
    high_user_rat_question_5 = next((q for q in questions if q.question_content == "High user rating 5"), None)

    user = create_user_in_db(username= 'userwithratings', password = 'XXXXXXXX', email= "testratings@mail.com")
    ratings = [
        QuestionRating(
            question_id=high_user_rat_question_1.id,
            user_id=user.id,
            rating=0.88
        ),
        QuestionRating(
            question_id=high_user_rat_question_2.id,
            user_id=user.id,
            rating=0.79
        ),
        QuestionRating(
            question_id=high_user_rat_question_3.id,
            user_id=user.id,
            rating=0.91
        ),
        QuestionRating(
            question_id=high_user_rat_question_4.id,
            user_id=user.id,
            rating=0.95
        ),
        QuestionRating(
            question_id=high_user_rat_question_5.id,
            user_id=user.id,
            rating=0.92
        )
    ]

    _db.session.bulk_save_objects(ratings)
    _db.session.commit()

    return {
        'user' : user,
        'questions' : questions_with_global_ratings,
        'ratings' : ratings,
    }