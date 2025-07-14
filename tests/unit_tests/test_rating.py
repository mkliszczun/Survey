from app.routes.rating import calculate_user_rating
from tests.conftest import test_client, login_user_for_test, create_user_in_db

def test_calculate_global_rating(test_client, questions_without_ratings, survey_data_for_one_question_with_big_score_diff, create_user_in_db):
    question_id = survey_data_for_one_question_with_big_score_diff['question_id']
    admin = create_user_in_db('admin3', 'password123', email = "testadminmail3@mail.com", role = 'admin')

    bad_response = test_client.post('/admin/api/rating', json={'question_id': question_id})  # to create app context
    login_user_for_test(test_client, admin)

    data = {
        'question_id': question_id
    }

    response = test_client.post('/admin/api/rating', json = data)

    data = response.get_json()

    assert response.status_code == 200
    assert data['success'] == True
    assert data['data'] == 7.0

def test_calculate_user_rating(test_client, questions_with_ratings, survey_data_for_one_question_with_big_score_diff, create_user_in_db):
    question_id = survey_data_for_one_question_with_big_score_diff['question_id']
    user_id = survey_data_for_one_question_with_big_score_diff['user_id']

    rating = calculate_user_rating(user_id, question_id)

    assert rating == 7