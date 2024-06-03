from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from exts import db
from models import User, Feed, Article
from namespaces.auth import auth_ns


def create_app(config):
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

    # shell context
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Feed': Feed, 'Article': Article}

    return app


# FOR LATER USE
# user serializer
# user_model = api.model('User', {
#     'id': fields.Integer(),
#     'username': fields.String(),
#     'email': fields.String(),
#     'password': fields.String()

# })

# feed serializer
# feed_model = api.model('Feed', {
#     'id': fields.Integer(),
#     'title': fields.String(),
#     'url': fields.String(),
# })

# article serializer
# article_model = api.model('Article', {
#     'id': fields.Integer(),
#     'title': fields.String(),
#     'author': fields.String(),
#     'pub_date': fields.DateTime(),
#     'url': fields.String(),
# })
