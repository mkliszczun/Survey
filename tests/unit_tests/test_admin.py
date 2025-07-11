from difflib import restore
from http.client import responses

from flask import session

from app import User
from app.extensions import db
from app.models import Question, QuestionRating, Choice
from tests.conftest import login_user_for_test, test_client


def test_admin_dashboard_not_logged(test_client, init_database):
    response = test_client.get("/admin/")
    assert response.status_code == 403

def test_admin_dashboard_regular_user(test_client, init_database, create_user_in_db):
    user = create_user_in_db('testuser', 'password123', email = "testusermail@mail.com", role='user')
    login_user_for_test(test_client, user)

    response = test_client.get("/admin/")
    assert response.status_code == 403

def test_admin_dashboard_admin(test_client, init_database, create_user_in_db):
    admin = create_user_in_db('admin', 'password123', email = "testadminmail@mail.com", role = 'admin')
    login_user_for_test(test_client, admin)

    response = test_client.get("/admin/")
    assert response.status_code == 200

def test_admin_add_question(test_client, init_database, create_user_in_db):
    admin = create_user_in_db('admin2', 'password123', email = "testadminmail2@mail.com", role = 'admin')
    login_user_for_test(test_client, admin)
    question1 = {
        'question_content' : 'test question content',
        'question_type' : 'choice',
        'choices' : ['test 1', 'test 2', 'test 3']
    }

    # choice question test
    response = test_client.post('/admin/add-question', json= question1)
    assert response.status_code == 201

    saved_question = Question.query.filter_by(question_content = 'test question content').first() #gets question by question_content for test below
                                                                                                  #done this way instead of get
    assert saved_question is not None                                                             # by id to avoid eventual future conflicts with id

    expected_num_of_choices = len(question1['choices'])

    assert len(saved_question.choices) == expected_num_of_choices

    assert saved_question.question_type == question1['question_type']

    retrieved_answer_contents = [choice.answer_content for choice in saved_question.choices]
    original_answers = question1['choices']

    assert retrieved_answer_contents == original_answers

    # text answer question test
    question2 = {
        'question_content' : 'test text question content',
        'question_type' : 'write'
    }

    response = test_client.post('/admin/add-question', json = question2)

    assert response.status_code == 201

    saved_question = Question.query.filter_by(question_content = 'test text question content').first()

    assert saved_question is not None
    assert saved_question.question_type == question2['question_type']
    assert saved_question.question_content == question2['question_content']

def test_admin_add_question_validation(test_client, init_database, create_user_in_db):

    admin = create_user_in_db('admin3', 'password123', email = "testadminmail3@mail.com", role = 'admin')
    login_user_for_test(test_client, admin)

    invalid_type_question = {
        'question_content' : 'just a wrong type',
        'question_type' : 'wrong type'
    }

    response = test_client.post('/admin/add-question', json = invalid_type_question)

    assert response.status_code == 400

    assert response.get_json()['message'] == 'invalid question type question not added'

    empty_question_content_question = {
        'question_content': '',
        'question_type': 'write'
    }

    response = test_client.post('admin/add-question', json = empty_question_content_question)

    assert response.status_code == 400
    assert response.get_json()['message'] == 'question_content empty - question not added'

def test_admin_delete_question(test_client, init_database, questions_with_ratings, create_user_in_db):

    question_to_delete_id = 1
    admin = create_user_in_db('admin4', 'password123', email="testadminmail4@mail.com", role='admin')
    login_user_for_test(test_client, admin)

    response = test_client.delete('/admin/delete_question', json = {'question_id' : question_to_delete_id})

    assert response.status_code == 200
    assert response.get_json()['message'] == 'Question removed'
    assert Question.query.get(question_to_delete_id) is None
    assert QuestionRating.query.filter_by(question_id = question_to_delete_id).first() is None
    assert Choice.query.filter_by(question_id = question_to_delete_id).first() is None