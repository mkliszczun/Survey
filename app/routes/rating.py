import math

import pandas as pd
from flask import Blueprint, jsonify, request
from flask_login import current_user
from sqlalchemy.orm import joinedload

from app import db
from app.models import Choice, Question, Survey, QuestionRating
from app.utils import admin_required

bp = Blueprint ('rating', __name__, url_prefix='/admin')

# TODO - add mood score to every survey to make the process faster
#@bp.route('/api/rating', methods = ['POST'])
#@admin_required
def calculate_question_global_rating(question_id_to_calculate):

    question_choices = Choice.query.options(joinedload(Choice.surveys)).filter_by(question_id = question_id_to_calculate).all()

    if not question_choices:
         return None, 'No choices found'

    data = []

    for choice in question_choices:
        #get all surveys where this choice occurs and from each survey choice for question with id 2
        surveys = choice.surveys

        data_to_append = {
            'choice_id' : choice.id,
            'mood_score' : []
        }
        for survey in surveys:
            for choice_in_survey in survey.choices: #TODO this loop is here to find mood score, when you'll change it
                if choice_in_survey.question_id == 2:         #TODO to be survey property it will need to be changed
                    data_to_append['mood_score'].append(int(choice_in_survey.answer_content))

        data.append(data_to_append)

    for item in data:
        scores = []
        if not scores:
            pass
        if item['mood_score']:
            scores.extend(item['mood_score'])
        print('scores:', scores)
        item['avg_mood_score'] = sum(scores) / len(scores) if scores else None

    df = pd.DataFrame(data)

    global_rating = df['avg_mood_score'].max() - df['avg_mood_score'].min()

    question = Question.query.filter_by(id = question_id_to_calculate).first()

    if question:
        if not isinstance(global_rating, (int, float)) or math.isnan(global_rating):
            #return jsonify({'success': False, 'message': 'global rating is not a valid number', 'global rating': global_rating}), 400
            return None, 'global rating is not a valid number'
        question.global_rating = global_rating
        db.session.commit()

    return global_rating, None

#TODO - make an ednpoint for global rating and refactor current endpoint for a method that will be called by endpoint

@bp.route('/api/rating', methods = ['POST'])
@admin_required
def global_rating():
    question_id = request.get_json()['question_id']
    calculate_question_global_rating(question_id)

    if question_id is None:
        return jsonify({'success' : False,'message': 'No question id provided'}), 400

    global_rating, error_message = calculate_question_global_rating(question_id)

    if not global_rating:
        return jsonify({'success' : False, 'message' : error_message}), 400

    return jsonify({'success' : True, 'message' : 'global rating calculated', 'data' : global_rating}), 200


@bp.route('/api/user_rating', methods = ['POST'])
@admin_required
def user_rating():
    print('user rating endpoint called')
    user_id = current_user.id
    question_id = request.get_json()['question_id']

    user_rating = calculate_user_rating(user_id, question_id)

    if user_rating is None:
        return jsonify({'success' : False, 'message': 'No user rating calculated'}), 400
    else:
        return jsonify({'success' : True, 'message' : 'user rating calculated', 'data' : user_rating}), 200

def calculate_user_rating(user_id, question_id):
    print('calculate user rating method called')
    #get all the surveys owned by the user that contain answer to this question
    surveys = Survey.query.filter(
        Survey.owner_id == user_id,
        Survey.choices.any(Choice.question_id == question_id)
    ).all()

    # from each survey get choice for that question and mood score
    data = []
    for survey in surveys:
        data_to_append = {
            'choice_id' : None,
            'mood_score' : None
        }
        for choice in survey.choices:
            if choice.question_id == question_id:
                data_to_append['choice_id'] = choice.id
            if choice.question_id == 2:
                data_to_append['mood_score'] = int(choice.answer_content)
        data.append(data_to_append)

        #data looks like this: [{'choice_id' : 1, 'mood_score' : 6},{...}...]
    df = pd.DataFrame(data)
    # group by choice_id and calculate average mood score
    df = df.groupby('choice_id')['mood_score'].mean().reset_index()
    # get the difference between max and min mood score
    max_mood_score = df['mood_score'].max()
    min_mood_score = df['mood_score'].min()
    # return the difference as user rating
    mood_score_dif = max_mood_score-min_mood_score

    try:
        rating = QuestionRating(rating = mood_score_dif, user_id = user_id, question_id = question_id)
        db.session.add(rating)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(e)

    return mood_score_dif

    pass
