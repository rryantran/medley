from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from feedparser import parse
from exts import db
from models import Feed, Article

# initialize namespace
feed_ns = Namespace('feed', description='Feed routes')

# feed serializer
feed_model = feed_ns.model('Feed', {
    'id': fields.Integer(),
    'title': fields.String(),
    'url': fields.String(),
})

# article serializer
article_model = feed_ns.model('Article', {
    'id': fields.Integer(),
    'title': fields.String(),
    'author': fields.String(),
    'pub_date': fields.DateTime(),
    'url': fields.String(),
})


@feed_ns.route('/<int:feed_id>/articles')
class FeedArticles(Resource):
    @feed_ns.marshal_with(article_model)
    def put(self, feed_id):
        '''update a feed's articles'''
        feed = db.session.execute(
            db.select(Feed).filter_by(id=feed_id)).scalar()

        if not feed:
            return {'message': 'Feed not found'}, 404

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
            else:
                break

            new_articles.append(new_article)

        if new_articles:
            feed.articles.extend(new_articles)
            db.session.commit()

        return new_articles, 200
