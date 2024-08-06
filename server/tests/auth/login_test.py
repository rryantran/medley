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
def mock_user():
    mock_user = User(username='mock_user', email='mock_user@mail.com',
                     password=generate_password_hash('password'))

    db.session.add(mock_user)
    db.session.commit()

    return mock_user


@pytest.fixture
def client(app):
    client = app.test_client()

    return client


def test_invalid_username(client, mock_user):
    json = {'username': '', 'password': 'password'}

    response = client.post('/auth/login', json=json)

    assert response.status_code == 401
    assert response.json['message'] == 'Invalid username or password'


def test_invalid_password(client, mock_user):
    json = {'username': 'mock_user', 'password': ''}

    response = client.post('/auth/login', json=json)

    assert response.status_code == 401
    assert response.json['message'] == 'Invalid username or password'


def test_valid_login(client, mock_user):
    json = {'username': 'mock_user', 'password': 'password'}

    response = client.post('/auth/login', json=json)

    assert response.status_code == 200
    assert response.json['message'] == 'Logged in successfully'

    cookies = response.headers.getlist('Set-Cookie')

    assert any('access_token_cookie' in cookie for cookie in cookies)
    assert any('refresh_token_cookie' in cookie for cookie in cookies)
