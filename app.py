from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tajny-klucz-123'  # W rzeczywistej apce użyj środowiskowych!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'api_login'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Model użytkownika
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def get_id(self):
        return str(self.id)


# Tworzenie bazy przy pierwszym uruchomieniu
@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
    print("Baza danych utworzona!")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods = ['POST'])
def api_register():
    data = request.get_json()

    #validation
    if not data and 'username' not in data or 'email' not in data or 'password' not in data:

        return jsonify({'success': False, 'message': 'Brak wszystkich wymaganych danych'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'message': 'Email zajęty'}), 409

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username = data['username'],
        email = data['email'],
        password = hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success' : True, 'message' : 'rejestracja udana'})
    except:
        return jsonify(({'success' : False, 'Message' : 'Błąd bazy danych'})), 500

@app.route('/api/login', methods = ['POST'])
def api_login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'success' : True, 'message' : 'zalogowano', 'redirect' : '/dashboard'})
    else:
        return jsonify({ 'success' : False ,'message' : 'Logowanie nie powiodło się'}), 401

@app.route('/api/logout', methods = ['POST'])
def api_logout():
    logout_user()
    return jsonify({'success' : True, 'redirect' : '/'})

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/survey')
@login_required
def survey():
    return render_template('survey.html')

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
    # Dodaj kolejne 8 pytań według tego schematu
]

@app.route('/api/questions')
@login_required
def get_questions():
    return jsonify(QUESTIONS)

@app.route('/api/submit-survey', methods=['POST'])
@login_required
def submit_survey():
    data = request.get_json()
    # Tutaj później dodamy logikę zapisywania do bazy
    print(f"Otrzymane odpowiedzi: {data}")
    return jsonify({"success": True})


if __name__ == '__main__':
    app.run(debug=True)