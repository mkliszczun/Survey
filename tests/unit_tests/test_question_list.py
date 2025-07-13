from tests.fixtures.users_fixtures import login_user_for_test


def test_get_top_user_questions(test_client,init_database,questions_with_ratings, create_user_in_db):

    context_activator = test_client.get('/') # no meaning besides activating context before loging user

    user = questions_with_ratings['user']
    login_user_for_test(test_client, user)

    response = test_client.get('/api/user_top_questions')
    data = response.get_json()['data']
    assert response.status_code == 200
    assert data is not None