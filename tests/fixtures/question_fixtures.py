import pytest

from app.models import Question, Choice, QuestionRating, db as _db


# TODO add question with id 2 as a mock of mood question and jump to survey fixtures - done


@pytest.fixture(scope='function')
def questions_without_ratings(init_database):
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

    return {
        'questions' : questions,
    }

@pytest.fixture(scope='function')
def questions_with_global_ratings(init_database):
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

    _db.session.add_all(questions)
    _db.session.commit()

    return {
        'questions': questions,
    }

@pytest.fixture(scope='function')
def questions_with_ratings(user_id):
    questions = questions_with_global_ratings()
    user = questions['user']
    ratings = [
        QuestionRating(
            question_id=1,
            user_id=user_id,
            rating=0.88
        ),
        QuestionRating(
            question_id=2,
            user_id=user_id,
            rating=0.79
        ),
        QuestionRating(
            question_id=3,
            user_id=user_id,
            rating=0.91
        ),
        QuestionRating(
            question_id=4,
            user_id=user_id,
            rating=0.95
        ),
        QuestionRating(
            question_id=5,
            user_id=user_id,
            rating=0.92
        ),
        QuestionRating(
            question_id=6,
            user_id=user_id,
            rating=0.81
        )
    ]

    _db.session.bulk_save_objects(ratings)
    _db.session.commit()

    return {
        'user' : user,
        'questions' : questions['questions'],
        'ratings' : ratings,
    }