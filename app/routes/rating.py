import math

import pandas as pd
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from app import db
from app.models import Choice, Question
from app.utils import admin_required

bp = Blueprint ('rating', __name__, url_prefix='/admin')

# TODO - add mood score to every survey to make the process faster
@bp.route('/api/rating', methods = ['POST'])
@admin_required
def calculate_question_global_rating():
    question_id_to_calculate = request.get_json()['question_id']

    question_choices = Choice.query.options(joinedload(Choice.surveys)).filter_by(question_id = question_id_to_calculate).all()

    if not question_choices:
        return jsonify({'message': 'No choices found'}), 404

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
            return jsonify({'success': False, 'message': 'global rating is not a valid number', 'global rating': global_rating}), 400
        question.global_rating = global_rating
        db.session.commit()

    return jsonify({'success' : True, 'message' : 'global rating calculated', 'data' : global_rating}), 200