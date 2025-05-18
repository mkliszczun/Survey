from flask import Blueprint, render_template

from app.utils import admin_required

bp = Blueprint ('survey_list', __name__, url_prefix='/admin')

@bp.route('/survey_list')
@admin_required
def admin_dashboard():
    return render_template('admin/survey_list.html')