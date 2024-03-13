from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from exts import db
from models import FeedLink

# initialize app
app = Flask(__name__)
app.config.from_object(DevConfig)

# initialize api
api = Api(app, doc='/docs')

# initialize db
db.init_app(app)

# initialize migrate
migrate = Migrate(app, db)

# serialize feedlink model
feedlink_model = api.model(
    'FeedLink',
    {
        'id': fields.Integer(),
        'name': fields.String(),
        'url': fields.String(),
    },

)


@api.route('/feedlinks')
class FeedLinkResource(Resource):
    @api.marshal_with(feedlink_model)
    def get(self):
        """Get all feed links"""
        feed_links = FeedLink.query.all()

        return feed_links

    @api.marshal_with(feedlink_model)
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
    return {'db': db, 'FeedLink': FeedLink}
