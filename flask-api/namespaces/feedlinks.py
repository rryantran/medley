from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from exts import db
from models import FeedLink

feedlink_ns = Namespace('feedlinks', description='Feed link operations')

# feed link model
feedlink_model = feedlink_ns.model(
    'FeedLink',
    {
        'id': fields.Integer(),
        'name': fields.String(),
        'url': fields.String(),
    },

)


@feedlink_ns.route('/feedlinks')
class FeedLinkResource(Resource):
    @feedlink_ns.marshal_with(feedlink_model)
    @jwt_required()
    def get(self):
        """Get all feed links"""
        feed_links = db.session.execute(db.select(FeedLink)).scalars().all()

        return feed_links

    @feedlink_ns.marshal_with(feedlink_model)
    @feedlink_ns.expect(feedlink_model)
    @jwt_required()
    def post(self):
        """Create a new feed link"""
        data = request.get_json()

        new_feed_link = FeedLink(
            name=data['name'],
            url=data['url']
        )

        new_feed_link.save()

        return new_feed_link, 201


@feedlink_ns.route('/feedlinks/<int:id>')
class FeedLinkResource(Resource):
    @feedlink_ns.marshal_with(feedlink_model)
    @jwt_required()
    def get(self, id):
        """Get a feed link"""
        feed_link = db.session.get(FeedLink, id)
        if feed_link is None:
            return 404

        return feed_link

    @feedlink_ns.marshal_with(feedlink_model)
    @feedlink_ns.expect(feedlink_model)
    @jwt_required()
    def put(self, id):
        """Update a feed link"""
        feed_link = db.session.get(FeedLink, id)
        if feed_link is None:
            return 404
        data = request.get_json()
        feed_link.update(data['name'], data['url'])

        return feed_link

    @feedlink_ns.marshal_with(feedlink_model)
    @jwt_required()
    def delete(self, id):
        """Delete a feed link"""
        feed_link = db.session.get(FeedLink, id)
        if feed_link is None:
            return 404
        feed_link.delete()

        return feed_link
