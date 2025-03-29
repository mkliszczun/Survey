# app/routes/admin.py
from flask import Blueprint, render_template
from app.utils import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')