from flask import request
from flask_restx import Namespace, Resource, fields
from exts import db
from models import User, Feed

# initialize namespace
user_ns = Namespace('user', description='User routes')

# user serializer
user_model = user_ns.model('User', {
    'id': fields.Integer(),
    'username': fields.String(),
    'email': fields.String(),
    'password': fields.String()

})

# feed serializer
feed_model = user_ns.model('Feed', {
    'id': fields.Integer(),
    'title': fields.String(),
    'url': fields.String(),
})


@user_ns.route('/<int:user_id>/feeds')
class UserFeeds(Resource):
    @user_ns.marshal_with(feed_model)
    def get(self, user_id):
        '''get all feeds for a user'''
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()

        if not user:
            return 404

        return user.feeds, 200

    @user_ns.expect(feed_model)
    def post(self, user_id):
        '''add a new feed for a user'''
        data = request.get_json()

        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()
        feed_exists = db.session.execute(
            db.select(Feed).filter_by(url=data['url'])).scalar()

        if not user:
            return {'message': 'User not found'}, 404
        if feed_exists:
            return {'message': 'Feed already exists'}, 400

        new_feed = Feed(
            title=data['title'],
            url=data['url']
        )

        user.feeds.append(new_feed)
        new_feed.save()

        return {'message': 'Feed added'}, 201


@user_ns.route('/<int:user_id>/feeds/<int:feed_id>')
class UserFeed(Resource):
    def delete(self, user_id, feed_id):
        '''delete a feed for a user'''
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()
        feed = db.session.execute(
            db.select(Feed).filter_by(id=feed_id)).scalar()

        if not user:
            return {'message': 'User not found'}, 404
        if not feed:
            return {'message': 'Feed not found'}, 404

        if feed in user.feeds:
            user.feeds.remove(feed)
            if user in feed.users:
                feed.users.remove(user)
            db.session.commit()
            if not feed.users:
                feed.delete()

        return {'message': 'Feed deleted'}, 200
