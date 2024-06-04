from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from config import DevConfig
from exts import db
from models import User, Feed, Article
from namespaces.auth import auth_ns
from namespaces.user import user_ns
from namespaces.feed import feed_ns


def create_app(config=DevConfig):
    # initialize app
    app = Flask(__name__)
    app.config.from_object(config)

    # initialize database
    db.init_app(app)

    # initialize migrate
    Migrate(app, db)

    # initialize jwt
    JWTManager(app)

    # initialize api
    api = Api(app)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(feed_ns)

    # shell context
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Feed': Feed, 'Article': Article}

    return app
