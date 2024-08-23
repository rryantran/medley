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


def test_missing_username(client):
    json = {'username': '', 'email': 'mock_user@mail.com',
            'password': 'password', 'confirm_password': 'password'}

    response = client.post('/auth/signup', json=json)

    assert response.status_code == 400
    assert response.get_json()['message'] == 'All fields are required'


def test_missing_email(client):
    json = {'username': 'mock_user', 'email': '',
            'password': 'password', 'confirm_password': 'password'}

    response = client.post('/auth/signup', json=json)

    assert response.status_code == 400
    assert response.get_json()['message'] == 'All fields are required'


def test_missing_password(client):
    json = {'username': 'mock_user', 'email': 'mock_user@mail.com',
            'password': '', 'confirm_password': 'password'}

    response = client.post('/auth/signup', json=json)

    assert response.status_code == 400
    assert response.get_json()['message'] == 'All fields are required'


def test_missing_confirm_password(client):
    json = {'username': 'mock_user', 'email': 'mock_user@mail.com',
            'password': 'password', 'confirm_password': ''}

    response = client.post('/auth/signup', json=json)

    assert response.status_code == 400
    assert response.get_json()['message'] == 'All fields are required'


def test_passwords_not_matching(client):
    json = {'username': 'mock_user', 'email': 'mock_user@mail.com',
            'password': 'password1', 'confirm_password': 'password2'}

    response = client.post('/auth/signup', json=json)

    assert response.status_code == 400
    assert response.get_json()['message'] == 'Passwords do not match'


def test_username_exists(client, mock_user):
    json = {'username': 'mock_user', 'email': 'user@mail.com',
            'password': 'password', 'confirm_password': 'password'}

    response = client.post('/auth/signup', json=json)

    assert response.status_code == 400
    assert response.get_json()['message'] == 'Username is already in use'


def test_email_exists(client, mock_user):
    json = {'username': 'user', 'email': 'mock_user@mail.com',
            'password': 'password', 'confirm_password': 'password'}

    response = client.post('/auth/signup', json=json)

    assert response.status_code == 400
    assert response.get_json()['message'] == 'Email is already in use'


def test_valid_signup(client):
    json = {'username': 'mock_user', 'email': 'mock_user@mail.com',
            'password': 'password', 'confirm_password': 'password'}

    response = client.post('/auth/signup', json=json)

    assert response.status_code == 201
    assert response.get_json()['message'] == 'User created successfully'
