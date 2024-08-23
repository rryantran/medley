import pytest
from werkzeug.security import generate_password_hash
from app import create_app
from config import TestConfig
from exts import db
from models import User


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()

    return client


def test_auth(client):
    signup_json = {'username': 'mock_user', 'email': 'mock_user@mail.com',
                   'password': 'password', 'confirm_password': 'password'}

    signup_response = client.post('/auth/signup', json=signup_json)

    assert signup_response.status_code == 201
    assert signup_response.get_json()['message'] == 'User created successfully'

    login_json = {'username': 'mock_user', 'password': 'password'}

    login_response = client.post('/auth/login', json=login_json)

    assert login_response.status_code == 200
    assert login_response.json['message'] == 'Logged in successfully'

    login_cookies = login_response.headers.getlist('Set-Cookie')

    assert any('access_token_cookie' in cookie for cookie in login_cookies)
    assert any('refresh_token_cookie' in cookie for cookie in login_cookies)

    logout_response = client.post('/auth/logout')

    assert logout_response.status_code == 200
    assert logout_response.json['message'] == 'Logged out successfully'

    logout_cookies = logout_response.headers.getlist('Set-Cookie')

    assert any('access_token_cookie=; ' in cookie for cookie in logout_cookies)
    assert any('refresh_token_cookie=; ' in cookie for cookie in logout_cookies)

    pass
