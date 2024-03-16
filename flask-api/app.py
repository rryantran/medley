from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from config import DevConfig
from exts import db
from models import FeedLink, User

# initialize app
app = Flask(__name__)
app.config.from_object(DevConfig)

# initialize api
api = Api(app, doc='/docs')

# initialize db
db.init_app(app)

# initialize migrate
migrate = Migrate(app, db)

# initialize jwt
jwt = JWTManager(app)

# feed link model
feedlink_model = api.model(
    'FeedLink',
    {
        'id': fields.Integer(),
        'name': fields.String(),
        'url': fields.String(),
    },

)


# sign up model
signup_model = api.model(
    'SignUp',
    {
        'email': fields.String(),
        'password': fields.String(),
        'password_2': fields.String(),
    },
)

# log in model
login_model = api.model(
    'LogIn',
    {
        'email': fields.String(),
        'password': fields.String(),
    },
)


@api.route('/signup')
class SignUp(Resource):
    @api.expect(signup_model)
    def post(self):
        """Create a new user"""
        data = request.get_json()

        # check if user already exists
        user = User.query.filter_by(email=data['email']).first()
        if user is not None:
            return {'message': 'Email already in use'}, 400

        # check if passwords match
        if data['password'] != data['password_2']:
            return {'message': 'Passwords do not match'}, 400

        new_user = User(
            email=data['email'], password=generate_password_hash(data['password']))

        new_user.save()

        return {'message': 'User created successfully'}, 201


@api.route('/login')
class LogIn(Resource):
    @api.expect(login_model)
    def post(self):
        """Log in a user"""
        data = request.get_json()

        # check if user exists and password is correct
        user = User.query.filter_by(email=data['email']).first()
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


@api.route('/feedlinks')
class FeedLinkResource(Resource):
    @api.marshal_with(feedlink_model)
    def get(self):
        """Get all feed links"""
        feed_links = FeedLink.query.all()

        return feed_links

    @api.marshal_with(feedlink_model)
    @api.expect(feedlink_model)
    def post(self):
        """Create a new feed link"""
        data = request.get_json()

        new_feed_link = FeedLink(
            name=data['name'],
            url=data['url']
        )

        new_feed_link.save()

        return new_feed_link, 201


@api.route('/feedlinks/<int:id>')
class FeedLinkResource(Resource):
    @api.marshal_with(feedlink_model)
    def get(self, id):
        """Get a feed link"""
        feed_link = FeedLink.query.get_or_404(id)

        return feed_link

    @api.marshal_with(feedlink_model)
    @api.expect(feedlink_model)
    def put(self, id):
        """Update a feed link"""
        feed_link = FeedLink.query.get_or_404(id)
        data = request.get_json()
        feed_link.update(data['name'], data['url'])

        return feed_link

    @api.marshal_with(feedlink_model)
    def delete(self, id):
        """Delete a feed link"""
        feed_link = FeedLink.query.get_or_404(id)
        feed_link.delete()

        return feed_link


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'FeedLink': FeedLink, 'User': User}
