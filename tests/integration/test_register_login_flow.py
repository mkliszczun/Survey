
def test_register_login_flow(test_client):
    data = {'username': 'flow_test_user', 'password': 'password', 'email' : 'flow@test.com'}
    response = test_client.post('/api/register', json = data)

    assert response.status_code == 200

    login_data = {'email': 'flow@test.com', 'password': 'password'}
    response = test_client.post('/api/login', json = login_data)

    assert response.status_code == 200
    assert response.get_json()['redirect'] == '/dashboard'

    response = test_client.get('/dashboard')
    assert response.status_code == 200
    assert b'Witaj, flow_test_user' in response.data

    response = test_client.post('/api/logout')
    assert response.status_code == 200
    assert response.get_json()['redirect'] == '/'