from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import Nullable, inspect

from ..extensions import db
from app.models import Question, Choice
from app.utils import admin_required


bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/add-question', methods = ['GET','POST'])
@admin_required
def add_question():

    if request.method == 'GET':
        return render_template('admin/add-question.html')
# ------------Validation------------
    if request.method == 'POST':
        data = request.get_json()

        if not data or 'question_content' not in data or 'question_type' not in data:
            return jsonify({'success': False, 'message': 'fill all required fields', }), 400

        if data['question_type'] == 'choice' and len(data['choices']) < 2:
            return jsonify({'success': False, 'message': 'question type choice must have at least 2 choices', }), 400

        if data['question_content'] == '':
            return jsonify({'success': False, 'message': 'question_content empty - question not added'}), 400

        new_question = Question(question_content=data['question_content'], question_type=data['question_type'])

        if new_question.question_type != 'write' and new_question.question_type != 'choice':

            return jsonify({'success': False, 'message': 'invalid question type question not added'}), 400

# ------------Validation------------
        if new_question.question_type == 'choice':

            for answer in data['choices']:
                choice = Choice(answer_content = answer)
                new_question.choices.append(choice)

            try:
                db.session.add(new_question)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Question Added'}),201

            except Exception as e:
                db.session.rollback()
                print(e)
                try:
                    inspector = inspect(db.engine)
                    for table_name in inspector.get_table_names():
                        print(f"\nTabela: {table_name}")
                        columns = inspector.get_columns(table_name)
                        for column in columns:
                            col_str = f"  - {column['name']} ({column['type']})"
                            if column.get('primary_key'):
                                col_str += " PRIMARY KEY"
                            print(col_str)
                except Exception as inspect_error:
                    print("Nie udało się pobrać struktury bazy danych:", inspect_error)
                return  jsonify({'success': False, 'message': 'something went wrong - question not added'}),500

        if new_question.question_type == 'write':
            try:
                db.session.add(new_question)
                db.session.commit()
                return jsonify({'success': True, 'message': 'Question Added'}),201

            except Exception as e:
                db.session.rollback()
                print(e)
                return jsonify({'success': False, 'message': 'something went wrong - question not added'}),500