from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__, template_folder='../../templates')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')