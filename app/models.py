from datetime import datetime
from email.policy import default
from sqlalchemy import nullsfirst
from sqlalchemy.orm import backref
from .database import db
from flask_login import UserMixin

survey_choices = db.Table('survey_choices',
    db.Column('survey_id', db.Integer, db.ForeignKey('survey.id'), primary_key=True),
    db.Column('choice_id', db.Integer, db.ForeignKey('choice.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    ROLES = ('user', 'admin')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), default = 'user', nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    surveys = db.relationship('Survey', backref = 'user', lazy = True)
    question_rating = db.relationship('QuestionRating', backref= 'user' ,lazy= True)


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable = False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id') , nullable=False)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question_content = db.Column(db.String(100), nullable = False)
    question_type = db.Column(db.String(15), nullable = False)
    choices = db.relationship('Choice', backref='question', lazy = False)
    global_rating = db.Column(db.Float, default = 0.0, nullable = False)

class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_content = db.Column(db.String(50), nullable = False)
    #surveys = db.Column(db.Integer, db.ForeignKey('survey.id'))
    surveys = db.relationship('Survey', secondary=survey_choices, back_populates='choices')

class Survey(db.Model):
    __tablename__ = 'survey'
    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    submission_date = db.Column(db.Integer, nullable = False)
    #choices = db.relationship('Choice')
    choices = db.relationship('Choice', secondary=survey_choices, back_populates='surveys')


class QuestionRating(db.Model):
    __tablename__ = 'question_rating'
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    rating = db.Column(db.Float, nullable = False)
