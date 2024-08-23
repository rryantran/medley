from datetime import datetime, timezone
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, create_access_token, set_access_cookies
from flask_migrate import Migrate
from flask_restx import Api
from config import DevConfig
from exts import db
from models import User, Feed, UserFeed, Article
from namespaces.auth import auth_ns
from namespaces.user import user_ns


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

    # token refresh
    @app.after_request
    def token_refresh(response):
        try:
            exp = get_jwt()['exp']
            curr_time = datetime.now(timezone.utc).timestamp()

            if exp - curr_time < 3600:
                current_user = get_jwt_identity()
                new_access_token = create_access_token(identity=current_user)
                response = jsonify({'message': 'Token refreshed'})
                set_access_cookies(response, new_access_token)
                response.status_code = 200

            return response
        except:
            return response

    # shell context
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Feed': Feed, 'UserFeed': UserFeed, 'Article': Article}

    return app
