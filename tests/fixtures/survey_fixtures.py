import dateutil.utils
import pytest

from app.models import Survey

#helper function to find the right choice for a question for survey
def find_mood_rating(mood_score, choices):

    for c in choices:
        if c.answer_content == mood_score:
            return c.id


#TODO find mood choices
@pytest.fixture
def survey_data_for_one_question_with_big_score_diff(init_database, create_user_in_db, questions_without_ratings):
    data = questions_without_ratings
    user = create_user_in_db(username= 'username', password = 'XXXXXXXX', email= "testmail@mail.com")
    question_to_fill_survey = None
    #make sure not mood question
    for q in data['questions']:
        if q.question_content != 'Mood question':
            question_to_fill_survey = q
            break

    choices = question_to_fill_survey.choices
    mood_choices = []

    #make sure it's mood question
    for q in data['questions']:
        if q.question_content == 'Mood question':
            mood_choices = q.choices
            break

    #needs to have answer with expected mood rating and choice from question
    surveys = [
        Survey(owner_id = user.id, submission_date = dateutil.utils.today(),
               choices = [choices[0], find_mood_rating(9, mood_choices)]),
        Survey(owner_id=user.id, submission_date=dateutil.utils.today(),
               choices=[choices[0], find_mood_rating(8, mood_choices)]),
        Survey(owner_id=user.id, submission_date=dateutil.utils.today(),
               choices=[choices[1], find_mood_rating(2, mood_choices)]),
        Survey(owner_id=user.id, submission_date=dateutil.utils.today(),
               choices=[choices[1], find_mood_rating(1, mood_choices)]),

    ]

    return { 'surveys' : surveys, 'user_id' : user.id, 'question_id' : question_to_fill_survey.id}