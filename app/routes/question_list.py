from flask import Blueprint, render_template, jsonify

from app.models import Question
from app.utils import admin_required

bp = Blueprint ('question_list', __name__, url_prefix='/admin')

@admin_required
@bp.route('/question_list')
def question_list():
    return render_template('admin/question_list.html')

@admin_required
@bp.route('/api/question_list')
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

    print(question_data)

    if question_data:
        return jsonify({'success' : True, 'data' : question_data}), 200
    else:
        return jsonify({'message': 'No questions found'}), 404