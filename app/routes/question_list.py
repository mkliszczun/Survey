from flask import Blueprint, render_template, jsonify
from flask_login import current_user

from app.models import Question, QuestionRating
from app.utils import admin_required

bp = Blueprint ('question_list', __name__)

@admin_required
@bp.route('/admin/question_list')
def question_list():
    return render_template('admin/question_list.html')

@admin_required
@bp.route('/admin/api/question_list')
def get_all_questions():
    questions = Question.query.all()
    question_data = []
    for question in questions:
        question_data.append({
            'id': question.id,
            'question_content': question.question_content,
            'question_type': question.question_type,
            'global_rating' : question.global_rating,
            'choices' : [choice.answer_content for choice in question.choices]
        })

    if question_data:
        return jsonify({'success' : True, 'data' : question_data}), 200
    else:
        return jsonify({'message': 'No questions found'}), 404

@bp.route('/user_top_questions')
def user_top_questions():
    return render_template('user_top_questions.html')

#gets all questions that have Question Rating with this user
#TODO - might add in the future pointing to choices with highest and lowest average mood score
@bp.route('/api/user_top_questions', methods = ['GET'])
def get_top_user_questions():
    print('getting top questions called')
    user_id = current_user.id
    questions = Question.query.join(QuestionRating).filter(QuestionRating.user_id == user_id).all()
    print('question len:')
    print(len(questions))
    ratings = QuestionRating.query.filter_by(user_id=user_id).all()
    print('ratings len:')
    print(len(ratings))
    question_data = []
    for q in questions:
        rating = int
        for r in ratings:
            if r.question_id == q.id:
                rating = r.rating
        question_data.append({
            'id': q.id,
            'question_content': q.question_content,
            'question_type': q.question_type,
            'global_rating' : q.global_rating,
            'choices' : [choice.answer_content for choice in q.choices],
            'rating' : rating
        })

    if question_data:
        return jsonify({'success' : True, 'data' : question_data}), 200
    else:
        print ('no questions found')
        print('user id: ' + str(user_id))
        print('questions: ' + str(questions))
        return jsonify({'message': 'No questions found'}), 404