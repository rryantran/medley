from datetime import datetime
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload
from flask_restx import Namespace, Resource, fields
from dotenv import load_dotenv
from feedparser import parse
from exts import db
from models import User, Feed, UserFeed, Article

# load environment variables
load_dotenv("../.env")

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

# article serializer
article_model = user_ns.model('Article', {
    'id': fields.Integer(),
    'title': fields.String(),
    'author': fields.String(),
    'pub_date': fields.DateTime(),
    'url': fields.String(),
})


@user_ns.route('/current')
class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        return {'user': user}, 200


@user_ns.route('/<int:user_id>/feeds')
class CurrentUserFeeds(Resource):
    @jwt_required()
    @user_ns.marshal_with(feed_model)
    def get(self, user_id):
        '''get all feeds for a user'''
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()

        if not user:
            return 404

        user_feeds = db.session.execute(
            db.select(UserFeed)
            .options(joinedload(UserFeed.feed))
            .filter_by(user_id=user.id)
        ).scalars().all()

        feeds = [
            {
                'id': user_feed.feed.id,
                'title': user_feed.title,
                'url': user_feed.feed.url
            }
            for user_feed in user_feeds
        ]

        return feeds, 200

    @jwt_required()
    @user_ns.expect(feed_model)
    def post(self, user_id):
        '''add a new feed for a user'''
        data = request.get_json()

        if not data['title'] or not data['url']:
            return {'message': 'All fields are required'}, 400

        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()
        feed = db.session.execute(
            db.select(Feed).filter_by(url=data['url'])).scalar()

        if not user:
            return {'message': 'User not found'}, 404
        if not feed:
            feed = Feed(url=data['url'])
            feed.save()

        user_feed = db.session.execute(db.select(UserFeed).filter_by(
            user_id=user_id, feed_id=feed.id)).scalar()

        if user_feed:
            return {'message': 'Feed already exists'}, 400

        new_user_feed = UserFeed(
            title=data['title'], user_id=user.id, feed_id=feed.id)
        new_user_feed.save()

        return {'message': 'Feed added'}, 201


@user_ns.route('/<int:user_id>/feeds/<int:feed_id>')
class CurrentUserFeed(Resource):
    @jwt_required()
    def put(self, user_id, feed_id):
        '''update a feed for a user'''
        data = request.get_json()

        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()
        feed = db.session.execute(
            db.select(Feed).filter_by(id=feed_id)).scalar()
        user_feed = db.session.execute(db.select(UserFeed).filter_by(
            user_id=user_id, feed_id=feed_id)).scalar()

        if not user:
            return {'message': 'User not found'}, 404
        if not feed:
            return {'message': 'Feed not found'}, 404
        if not user_feed:
            return {'message': 'Feed not found'}, 404

        if not data['title'] or not data['url']:
            return {'message': 'All fields are required'}, 400

        user_feed.update(data['title'])
        feed.update(data['url'])

        return {'message': 'Feed updated'}, 200

    @jwt_required()
    def delete(self, user_id, feed_id):
        '''delete a feed for a user'''
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()
        feed = db.session.execute(
            db.select(Feed).filter_by(id=feed_id)).scalar()
        user_feed = db.session.execute(db.select(UserFeed).filter_by(
            user_id=user_id, feed_id=feed_id)).scalar()

        if not user:
            return {'message': 'User not found'}, 404
        if not feed:
            return {'message': 'Feed not found'}, 404
        if not user_feed:
            return {'message': 'Feed not found'}, 404

        if user_feed in user.feeds:
            user.feeds.remove(user_feed)
            user_feed.delete()
            if not feed.users:
                feed.delete()

        return {'message': 'Feed deleted'}, 200


@user_ns.route('/<int:user_id>/articles')
class CurrentUserArticles(Resource):
    @jwt_required()
    @user_ns.marshal_with(article_model)
    def get(self, user_id):
        '''get all articles for a user'''
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()

        if not user:
            return {'message': 'User not found'}, 404

        user_feeds = db.session.execute(
            db.select(UserFeed)
            .options(joinedload(UserFeed.feed))
            .filter_by(user_id=user.id)
        ).scalars().all()

        articles = db.session.execute(
            db.select(Article)
            .options(joinedload(Article.feed))
            .filter(Article.feed_id.in_([feed.feed.id for feed in user_feeds]))
        ).scalars().all()

        return articles, 200

    @jwt_required()
    def put(self, user_id):
        '''update all articles for a user'''
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()

        if not user:
            return {'message': 'User not found'}, 404

        user_feeds = db.session.execute(
            db.select(UserFeed)
            .options(joinedload(UserFeed.feed))
            .filter_by(user_id=user.id)
        ).scalars().all()

        for feed in user_feeds:
            parsed_feed = parse(feed.feed.url)
            for entry in parsed_feed.entries:
                article = db.session.execute(
                    db.select(Article).filter_by(url=entry.link)).scalar()

                if not article:
                    new_article = Article(
                        title=entry.title,
                        author=entry.author,
                        pub_date=datetime.strptime(
                            entry.published, '%a, %d %b %Y %H:%M:%S %z'),
                        url=entry.link,
                        source=feed.title,
                        feed_id=feed.feed.id
                    )
                    new_article.save()
                else:
                    break

        return {'message': 'Articles updated'}, 200
