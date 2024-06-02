from flask import Flask
from flask_restx import Api, Resource
from config import DevConfig

# initialize app
app = Flask(__name__)
app.config.from_object(DevConfig)

# initialize api
api = Api(app)


@api.route('/test')
class Test(Resource):
    def get(self):
        return {'message': 'TESTING'}


if __name__ == '__main__':
    app.run()
