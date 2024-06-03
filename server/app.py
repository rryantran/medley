from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from flask_migrate import Migrate
from flask_restx import Api, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
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

# initialize jwt
jwt = JWTManager(app)

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

# sign up serializer
signup_model = api.model('SignUp', {
    'username': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
    'confirm_password': fields.String()
})

# log in serializer
login_model = api.model('LogIn', {
    'username': fields.String(),
    'password': fields.String()
})


# test route
@api.route('/test')
class Test(Resource):
    def get(self):
        '''get test message'''
        return {'message': 'TESTING'}


# signup route
@api.route('/signup')
class SignUp(Resource):
    @api.expect(signup_model)
    def post(self):
        '''create a new user'''
        data = request.get_json()

        if data['password'] != data['confirm_password']:
            return {'message': 'Password does not match'}, 400

        username_exists = db.session.execute(db.select(User).filter_by(
            username=data['username'])).scalar()
        email_exists = db.session.execute(
            db.select(User).filter_by(email=data['email'])).scalar()

        if username_exists:
            return {'message': 'Username already in use'}, 400
        elif email_exists:
            return {'message': 'Email already in use'}, 400

        new_user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'])
        )

        new_user.save()

        return {'message': 'User created successfully'}, 201


# login route
@api.route('/login')
class LogIn(Resource):
    @api.expect(login_model)
    def post(self):
        '''log in a user'''
        data = request.get_json()

        user = db.session.execute(db.select(User).filter_by(
            username=data['username'])).scalar()

        if not user or not check_password_hash(user.password, data['password']):
            return {'message': f'Invalid username or password'}, 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {'message': 'Logged in successfully', 'access_token': access_token, 'refresh_token': refresh_token}, 200


# shell context
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Feed': Feed, 'Article': Article}


if __name__ == '__main__':
    app.run()
