from datetime import date

from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import not_

from .rating import calculate_user_rating, calculate_question_global_rating
from ..models import Question, QuestionRating, Survey, Choice
from ..extensions import db

bp = Blueprint('survey', __name__)

def check_if_user_has_answered_today(user_id):
    todays_survey = Survey.query.filter_by(owner_id = user_id, submission_date = date.today()).first()
    if todays_survey:
        return jsonify({'success' : False, 'message' : 'Wypełniłeś już dzisiaj ankietę'})
    else:
        return False

@bp.route('/survey')
@login_required
def survey():
    survey_check = check_if_user_has_answered_today(current_user.id)
    if survey_check:
        flash("Wypełniłeś już dzisiaj ankietę.", "error")
        return redirect(url_for("main.dashboard"))
    else:
        return render_template('survey.html')

# Returns list of 10 questions
# Returns 5 with highest rating to user
# 2 wildcards
# 1 question regarding how user feels
# 2 global highest rank questions
@bp.route('/api/questions')
@login_required
def get_questions():

    QUESTION_ABOUT_HUMOR_ID = 2

    question_about_humor = [Question.query.filter_by(id = QUESTION_ABOUT_HUMOR_ID).first()]
    excluded_ids = [QUESTION_ABOUT_HUMOR_ID]

    top_five_question_ratings = (
        QuestionRating.query
        .filter(~QuestionRating.question_id.in_(excluded_ids))
        .filter_by(user_id = current_user.id)
        .order_by(QuestionRating.rating.desc())
        .limit(5)
        .all()
    )

    top_five_questions = []

    if len(top_five_question_ratings) == 5:
        for r in top_five_question_ratings:
            print(r.rating)
        top_five_questions = Question.query.filter(
        Question.id.in_([qr.id for qr in top_five_question_ratings])).all()

    # If there's no rating yet - first survey - it returns 5 random questions instead of 2.
    # After first survey questions will get rating
    else:
        top_five_questions = (
            Question
            .query.filter(not_(Question.id.in_(excluded_ids)))
            .order_by(db.func.random())
            .limit(5)
            .all())

    ids_to_exclude = [q.id for q in top_five_questions]
    excluded_ids.extend(ids_to_exclude)

    two_wildcards = (
        Question.query
        .filter(not_(Question.id.in_(excluded_ids)))
        .order_by(db.func.random())
        .limit(2)
        .all()
    )

    ids_to_exclude = [q.id for q in two_wildcards]
    excluded_ids.extend(ids_to_exclude)

    global_two_questions = (
        Question.query
        .filter(not_(Question.id.in_(excluded_ids)))
        .order_by(Question.global_rating.desc()).limit(2).all()
    )

    questions_to_return = top_five_questions + two_wildcards + global_two_questions + question_about_humor

    return jsonify([{
        'id': q.id,
        'question_content': q.question_content,
        'question_type': q.question_type,
        'global_rating': q.global_rating,
        'choices': [
        {
            'id': c.id,
            'answer_content': c.answer_content
        } for c in q.choices]
    } for q in questions_to_return]), 200

@bp.route('/api/submit-survey', methods=['POST'])
@login_required
def submit_survey():

    survey_check = check_if_user_has_answered_today(current_user.id)
    if survey_check:
        return survey_check, 400

    try:
        data = request.get_json()
        user_id = current_user.id
        choice_ids = list(choice['id'] for choice in data)

        choices = list(Choice.query.filter(Choice.id.in_(choice_ids)))

        if len(choices) != len(choice_ids): #check if all ids found
            found_ids = {c.id for c in choices}
            missing_ids = [cid for cid in choice_ids if cid not in found_ids]
            raise ValueError(f"Choices not found for IDs: {missing_ids}")

        print(choice_ids)

        survey_to_save = Survey(owner_id = user_id, submission_date = date.today(), choices = choices)
        db.session.add(survey_to_save)
        db.session.commit()

        question_ids = list(set([c.question_id for c in choices]))
        questions = Question.query.filter(Question.id.in_(question_ids)).all()

        #print size of questions
        user_rat_num = 0
        global_rat_num = 0

        for q in questions:
            if q.id != 2:
               calculate_user_rating(current_user.id, q.id)
               user_rat_num += 1

        for q in questions:
            if q.id != 2:
               calculate_question_global_rating(q.id)
               global_rat_num += 1

        return jsonify({"success": True}), 200

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"success": False, "error": str(e)}), 500