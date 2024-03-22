from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from config import DevConfig
from exts import db
from models import Article, FeedLink, User
from namespaces.articles import article_ns
from namespaces.auth import auth_ns
from namespaces.feedlinks import feedlink_ns

# initialize app
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # initialize api
    api = Api(app, doc='/docs')
    api.add_namespace(article_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(feedlink_ns)

    # initialize db
    db.init_app(app)

    # initialize migrate
    migrate = Migrate(app, db)

    # initialize jwt
    jwt = JWTManager(app)

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Article': Article, 'FeedLink': FeedLink, 'User': User}
    
    return app
