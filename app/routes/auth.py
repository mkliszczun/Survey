from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from ..models import User
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()

    # validation
    if not data and 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Brak wszystkich wymaganych danych'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Email zajęty'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'rejestracja udana'})
    except:
        return jsonify(({'success': False, 'Message': 'Błąd bazy danych'})), 500


@bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'success': True, 'message': 'zalogowano', 'redirect': '/dashboard'})
    else:
        return jsonify({'success': False, 'message': 'Logowanie nie powiodło się'}), 401

@bp.route('/api/logout', methods=['POST'])
def api_logout():
    logout_user()
    return jsonify({'success': True, 'redirect': '/'})