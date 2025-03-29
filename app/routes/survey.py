from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user
from ..models import Answer
from ..extensions import db

bp = Blueprint('survey', __name__)

QUESTIONS = [
    {
        "id": 1,
        "text": "Ile godzin dzisiaj spałeś(-aś)?",
        "type": "radio",
        "options": ["4-5", "5-6", "7", "8", "9-10"]
    },
    {
        "id": 2,
        "text": "Jak wyglądał Twój poziom aktywności fizycznej dzisiaj?",
        "type": "radio",
        "options": ["brak", "lekka", "umiarkowana", "instensywna"]
    },
    {
        "id":3,
        "text": "W jaki sposób się dzisiaj odżywiałeś(-aś)",
        "type": "radio",
        "options": ["niezdrowo", "umiarkowanie niezdrowo", "umiarkowanie zdrowo", "zdrowo"]
    },
    {
        "id": 4,
        "text": "Jak często w ciągu dnia miałeś(-aś) interakcje z innymi ludźmi?",
        "type": "radio",
        "options": ["brak", "sporadycznie", "umiarkowanie", "instensywnie"]
    },
    {
        "id": 5,
        "text": "Ile miałeś dzisiaj czasu na relaks?",
        "type": "radio",
        "options": ["brak", "kilka/kilkanaście minut", "1-2 h", "więcej niż 2 h"]
    },
    {
        "id": 6,
        "text": "Jak dużo czasu spędziłeś(aś) dzisiaj na świeżym powietrzu?",
        "type": "radio",
        "options": ["brak", "10-30 min", "30-60 min", "więcej niż 1h"]
    },
    {
        "id": 7,
        "text": "Ile czasu byłeś(-aś) dzisiaj poza domem?",
        "type": "radio",
        "options": ["brak", "mniej niż 1h", "1-8 h", "więcej niż 8 h"]
    },
    {
        "id": 8,
        "text": "Ile miałeś dzisiaj czasu na relaks?",
        "type": "radio",
        "options": ["brak", "kilka/kilkanaście minut", "1-2 h", "więcej niż 2 h"]
    },
    {
        "id": 9,
        "text": "Ile posiłków dzisiaj jadłeś?",
        "type": "radio",
        "options": ["2", "3", "4", "5"]
    },
    {
        "id": 10,
        "text": "Jak oceniach twoje samopoczucie dzisiejszego dnia?",
        "type": "radio",
        "options": ["fatalne", "słabe", "dobre", "bardzo dobre"]
    }
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