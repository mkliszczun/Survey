import dateutil.utils
import pytest
from app.models import db as _db, User

from app.models import Survey

#helper function to find the right choice for a question for survey
def find_mood_rating(mood_score, choices):

    for c in choices:
        if c.answer_content == mood_score:
            print('mood rating found in helper function')
            return c



@pytest.fixture
def survey_data_for_one_question_with_big_score_diff(init_database, create_user_in_db, questions_without_ratings):
    data = questions_without_ratings

    _db.session.query(User).delete()
    _db.session.commit()

    _db.session.expire_all()

    user = create_user_in_db(username= 'username', password = 'XXXXXXXX', email= "testmail@mail.com")
    question_to_fill_survey = None

    #make sure not mood question
    for q in data['questions']:
        if q.question_content != 'Mood question':
            question_to_fill_survey = q
            print('normal question found')
            break

    choices = question_to_fill_survey.choices
    mood_choices = []

    #make sure it's mood question
    for q in data['questions']:
        if q.question_content == 'Mood question':
            mood_choices = q.choices
            print("mood choice found")
            break
    print(len(mood_choices))
    for c in mood_choices:
        print(c.answer_content)

    mood_score_9 = _db.session.merge(find_mood_rating('9', mood_choices))
    mood_score_8 = _db.session.merge(find_mood_rating('8', mood_choices))
    mood_score_2 = _db.session.merge(find_mood_rating('2', mood_choices))
    mood_score_1 = _db.session.merge(find_mood_rating('1', mood_choices))

    #needs to have answer with expected mood rating and choice from question
    surveys = [
        Survey(owner_id = user.id, submission_date = dateutil.utils.today(),
               choices = [choices[0], mood_score_9]),
        Survey(owner_id=user.id, submission_date=dateutil.utils.today(),
               choices=[choices[0], mood_score_8]),
        Survey(owner_id=user.id, submission_date=dateutil.utils.today(),
               choices=[choices[1], mood_score_2]),
        Survey(owner_id=user.id, submission_date=dateutil.utils.today(),
               choices=[choices[1], mood_score_1])
    ]

    _db.session.add_all(surveys)
    _db.session.commit()

    return { 'surveys' : surveys, 'user_id' : user.id, 'question_id' : question_to_fill_survey.id}