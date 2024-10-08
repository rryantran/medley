from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
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


# sign up route
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

        #
        if username_exists:
            return {'message': 'Username is already in use'}, 400
        elif email_exists:
            return {'message': 'Email is already in use'}, 400

        new_user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'])
        )

        db.session.add(new_user)
        db.session.commit()

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

        response = jsonify(
            {'message': 'Logged in successfully', 'id': user.id})

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        response.status_code = 200

        return response


# logout route
@auth_ns.route('/logout')
class LogOut(Resource):
    def post(self):
        '''log out a user'''
        response = jsonify({'message': 'Logged out successfully'})

        unset_jwt_cookies(response)

        response.status_code = 200

        return response
