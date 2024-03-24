from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from models import User

auth_ns = Namespace('auth', description='Authentication operations')

# sign up model
signup_model = auth_ns.model(
    'SignUp',
    {
        'email': fields.String(),
        'password': fields.String(),
        'password_2': fields.String(),
    },
)

# log in model
login_model = auth_ns.model(
    'LogIn',
    {
        'email': fields.String(),
        'password': fields.String(),
    },
)


@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        """Create a new user"""
        data = request.get_json()

        # check if user already exists
        user = db.session.execute(
            db.select(User).filter_by(email=data['email'])).scalar()
        if user is not None:
            return {'message': 'Email already in use'}, 400

        # check if passwords match
        if data['password'] != data['password_2']:
            return {'message': 'Passwords do not match'}, 400

        new_user = User(
            email=data['email'], password=generate_password_hash(data['password']))

        new_user.save()

        return {'message': 'User created successfully'}, 201


@auth_ns.route('/login')
class LogIn(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Log in a user"""
        data = request.get_json()

        # check if user exists and password is correct
        user = db.session.execute(
            db.select(User).filter_by(email=data['email'])).scalar()
        if user is None or not check_password_hash(user.password, data['password']):
            return {'message': 'Invalid email or password'}, 400

        # create access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {
            'message': 'Logged in successfully',
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


@auth_ns.route('/refresh')
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Refresh the access token"""
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {'access_token': new_access_token}, 200
