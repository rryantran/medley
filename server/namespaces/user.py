from datetime import datetime
from flask import request, current_app
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
    'source': fields.String(),
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
            return {'message': 'User not found'}, 404

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

        if not user:
            return {'message': 'User not found'}, 404

        feed = db.session.execute(
            db.select(Feed).filter_by(url=data['url'])).scalar()

        if not feed:
            feed = Feed(url=data['url'])
            db.session.add(feed)
            db.session.commit()

        user_feed = db.session.execute(db.select(UserFeed).filter_by(
            user_id=user_id, feed_id=feed.id)).scalar()

        if user_feed:
            return {'message': 'Feed already exists'}, 400

        new_user_feed = UserFeed(
            title=data['title'], user_id=user.id, feed_id=feed.id)
        db.session.add(new_user_feed)
        db.session.commit()

        return {'message': 'Feed added'}, 201


@user_ns.route('/<int:user_id>/feeds/<int:feed_id>')
class CurrentUserFeed(Resource):
    @jwt_required()
    def put(self, user_id, feed_id):
        '''update a feed for a user'''
        data = request.get_json()

        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()

        if not user:
            return {'message': 'User not found'}, 404

        feed = db.session.execute(
            db.select(Feed).filter_by(id=feed_id)).scalar()

        if not feed:
            return {'message': 'Feed not found'}, 404

        user_feed = db.session.execute(db.select(UserFeed).filter_by(
            user_id=user_id, feed_id=feed_id)).scalar()

        if not user_feed:
            return {'message': 'Feed not found'}, 404

        if not data['title'] or not data['url']:
            return {'message': 'All fields are required'}, 400

        if parse(data['url']).bozo:
            return {'message': 'Invalid feed url'}, 400

        user_feed.title = data['title']
        feed.url = data['url']

        db.session.commit()

        return {'message': 'Feed updated'}, 200

    @jwt_required()
    def delete(self, user_id, feed_id):
        '''delete a feed for a user'''
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()

        if not user:
            return {'message': 'User not found'}, 404

        feed = db.session.execute(
            db.select(Feed).filter_by(id=feed_id)).scalar()

        if not feed:
            return {'message': 'Feed not found'}, 404

        user_feed = db.session.execute(db.select(UserFeed).filter_by(
            user_id=user_id, feed_id=feed_id)).scalar()

        articles_to_delete = db.session.execute(
            db.select(Article).filter_by(feed_id=feed_id).filter(
                Article.userfeeds.any(user_id=user_id))
        ).scalars().all()

        for article in articles_to_delete:
            article.userfeeds.remove(user_feed)

            if not article.userfeeds:
                db.session.delete(article)

        if user_feed in user.feeds:
            user.feeds.remove(user_feed)
            db.session.delete(user_feed)

            if not feed.users:
                db.session.delete(feed)

        db.session.commit()

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

        return_articles = [
            {
                'id': article.id,
                'title': article.title,
                'author': article.author,
                'pub_date': article.pub_date,
                'source': [
                    user_feeds.title for user_feeds in article.userfeeds if user_feeds.user_id == user_id][0],
                'url': article.url
            }
            for article in articles
        ]

        return return_articles, 200

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

        for user_feed in user_feeds:
            parsed_feed = parse(user_feed.feed.url)

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
                        feed_id=user_feed.feed.id
                    )

                    new_article.userfeeds.append(user_feed)
                    db.session.add(new_article)
                else:
                    if user_feed not in article.userfeeds:
                        article.userfeeds.append(user_feed)

        db.session.commit()

        return {'message': 'Articles updated'}, 200
