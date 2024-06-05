from datetime import datetime
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from dotenv import load_dotenv
from feedparser import parse
from exts import db
from models import User, Feed, Article

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


@jwt_required()
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
        db.session.commit()

        return {'message': 'Feed added'}, 201


@jwt_required()
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
            if not feed.users:
                feed.delete()

        return {'message': 'Feed deleted'}, 200


@jwt_required()
@user_ns.route('/<int:user_id>/articles')
class UserArticles(Resource):
    @user_ns.marshal_with(article_model)
    def get(self, user_id):
        '''get all articles for a user'''
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()

        if not user:
            return {'message': 'User not found'}, 404

        all_articles = []

        for feed in user.feeds:
            all_articles.extend(feed.articles)

        return all_articles, 200

    def put(self, user_id):
        '''update all articles for a user'''
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)).scalar()

        if not user:
            return {'message': 'User not found'}, 404

        for feed in user.feeds:
            parsed = parse(feed.url)
            new_articles = []

            for entry in parsed.entries:
                article_exists = db.session.execute(
                    db.select(Article).filter_by(url=entry.link)).scalar()

                if not article_exists:
                    new_article = Article(
                        title=entry.title,
                        author=entry.author,
                        pub_date=datetime.strptime(
                            entry.published, '%a, %d %b %Y %H:%M:%S %z'),
                        url=entry.link
                    )

                    new_articles.append(new_article)
                else:
                    break

            if new_articles:
                feed.articles.extend(new_articles)
                db.session.commit()

        return {'message': 'Articles updated'}, 200
