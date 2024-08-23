import pytest
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


def test_logout(client):
    response = client.post('/auth/logout')

    assert response.status_code == 200
    assert response.json['message'] == 'Logged out successfully'

    cookies = response.headers.getlist('Set-Cookie')

    assert any('access_token_cookie=; ' in cookie for cookie in cookies)
    assert any('refresh_token_cookie=; ' in cookie for cookie in cookies)
