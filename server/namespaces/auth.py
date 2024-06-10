from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db
from models import User

# initialize namespace
auth_ns = Namespace('auth', description='Authentication routes')

# sign up serializer
signup_model = auth_ns.model('SignUp', {
    'username': fields.String(),
    'email': fields.String(),
    'password': fields.String(),
    'confirm_password': fields.String()
})

# log in serializer
login_model = auth_ns.model('LogIn', {
    'username': fields.String(),
    'password': fields.String()
})


# signup route
@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        '''create a new user'''
        data = request.get_json()

        if not data['username'] or not data['email'] or not data['password'] or not data['confirm_password']:
            return {'message': 'All fields are required'}, 400

        if data['password'] != data['confirm_password']:
            return {'message': 'Passwords do not match'}, 400

        username_exists = db.session.execute(db.select(User).filter_by(
            username=data['username'])).scalar()
        email_exists = db.session.execute(
            db.select(User).filter_by(email=data['email'])).scalar()

        if username_exists:
            return {'message': 'Username is already in use'}, 400
        elif email_exists:
            return {'message': 'Email is already in use'}, 400

        new_user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'])
        )

        new_user.save()

        return {'message': 'User created successfully'}, 201


# login route
@auth_ns.route('/login')
class LogIn(Resource):
    @auth_ns.expect(login_model)
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


# refresh token route
@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        '''refresh access token'''
        current_user = get_jwt_identity()

        new_access_token = create_access_token(identity=current_user)

        return {'access_token': new_access_token}, 200
