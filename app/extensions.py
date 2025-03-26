# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import User
from .database import db


# db = SQLAlchemy()
login_manager = LoginManager()

def load_user(user_id):
    return User.query.get(int(user_id))