from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

# initialize app
app = Flask(__name__)
app.config.from_object(DevConfig)

# initialize api
api = Api(app)

# initialize db
db = SQLAlchemy()
db.init_app(app)

# test resource
class Test(Resource):
    def get(self):
        return {'test': 'this is a test'}

api.add_resource(Test, '/test')
