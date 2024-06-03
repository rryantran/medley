from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api, Resource, fields
from config import DevConfig
from exts import db
from models import User, Feed, Article

# initialize app
app = Flask(__name__)
app.config.from_object(DevConfig)

# initialize api
api = Api(app)

# initlialize database
db.init_app(app)

# initialize migration
migrate = Migrate(app, db)

# user serializer
user_model = api.model('User', {
    'id': fields.Integer(),
    'username': fields.String(),
    'email': fields.String(),
    'password': fields.String()

})

# feed serializer
feed_model = api.model('Feed', {
    'id': fields.Integer(),
    'title': fields.String(),
    'url': fields.String(),
})

# article serializer
article_model = api.model('Article', {
    'id': fields.Integer(),
    'title': fields.String(),
    'author': fields.String(),
    'pub_date': fields.DateTime(),
    'url': fields.String(),
})


# test route
@api.route('/test')
class Test(Resource):
    def get(self):
        return {'message': 'TESTING'}


# shell context
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Feed': Feed, 'Article': Article}


if __name__ == '__main__':
    app.run()
