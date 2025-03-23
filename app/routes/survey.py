from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user
from ..models import Answer
from ..extensions import db

bp = Blueprint('survey', __name__)

QUESTIONS = [
    {
        "id": 1,
        "text": "Jak często uprawiasz sport?",
        "type": "radio",
        "options": ["Codziennie", "Kilka razy w tygodniu", "Raz w miesiącu", "Nigdy"]
    },
    {
        "id": 2,
        "text": "Ulubiony rodzaj książek:",
        "type": "text"
    },
    # + 8 questions soon
]

@bp.route('/survey')
@login_required
def survey():
    return render_template('survey.html')

@bp.route('/api/questions')
@login_required
def get_questions():
    return jsonify(QUESTIONS)

@bp.route('/api/submit-survey', methods=['POST'])
@login_required
def submit_survey():
    try:
        data = request.get_json()

        for question_id, answer in data.items():
            new_answer = Answer(
                user_id=current_user.id,
                question_id=int(question_id.replace('q', '')),  # np. "q2" → 2
                answer_text=str(answer)
            )
            db.session.add(new_answer)

        db.session.commit()
        return jsonify({"success": True})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500