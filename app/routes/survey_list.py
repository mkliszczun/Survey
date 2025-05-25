from flask import Blueprint, render_template, jsonify
from sqlalchemy.orm import joinedload
from flask_login import current_user

from app.models import Survey
from app.utils import admin_required

bp = Blueprint ('survey_list', __name__, url_prefix='/admin')

@bp.route('/survey_list')
@admin_required
def survey_list():

    return render_template('admin/survey-list.html'), 200

@bp.route('/api/survey_list')
@admin_required
def get_surveys():
    user_id = current_user.id
    surveys = Survey.query.filter_by(owner_id = user_id).options(joinedload(Survey.choices)).all()
    survey_data = []
    for survey in surveys:
        survey_data.append({
            'id': survey.id,
            'owner_id': survey.owner_id,
            'submission_date': survey.submission_date,
            'choices':  [choice.answer_content for choice in survey.choices]
        })

    if survey_data:
        return jsonify({'success' : True, 'data' : survey_data}), 200

    else:
        print('surveys not found')
        return jsonify({'message': 'No surveys found'}), 404