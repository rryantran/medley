from flask import Flask
from flask_restx import Api, Resource
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
