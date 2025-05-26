import pandas as pd
from flask import Blueprint, jsonify, request

from app import db
from app.models import Choice, Question
from app.utils import admin_required

bp = Blueprint ('rating', __name__, url_prefix='/admin')


# TODO - add mood score to every survey to make the process faster
@bp.route('/api/rating')
@admin_required
def calculate_question_global_rating():
    question_id_to_calculate = request.get_json()['question_id']

    question_choices = Choice.query.filter_by(question_id = question_id_to_calculate).all()

    if not question_choices:
        return jsonify({'message': 'No choices found'}), 404

    data = []

    for choice in question_choices:
        #get all surveys where this choice occurs and from each survey choice for question with id 2
        surveys = choice.surveys #might not be included because of lazy loading
        data_to_append = {
            'choice_id' : choice.id,
            'mood_score' : []
        }
        for survey in surveys:
            for choice_in_survey in survey.choices: #TODO this loop is here to find mood score, when you'll change it
                if choice.question_id == 2:         #TODO to be survey property it will need to be changed
                    data_to_append[0]['mood_score'].append(int(choice.answer_content))

        data.append(data_to_append)

    for item in data:
        scores = item['mood_score']
        item['avg_mood_score'] = sum(scores) / len(scores) if scores else None

    df = pd.DataFrame(data)

    global_rating = df['avg_mood_score'].max() - df['avg_mood_score'].min()

    question = Question.query.filter_by(id = question_id_to_calculate).first()

    if question:
        question.global_rating = global_rating
        db.session.commit()

    return jsonify({'success' : True, 'message' : 'global rating calculated', 'data' : global_rating}), 200