from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required
from flask_migrate import Migrate
from flask_restx import Api, Namespace, Resource, fields
from datetime import datetime
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from config import DevConfig
from exts import db
from models import Article, FeedLink, User

article_ns = Namespace('articles', description='Article operations')

# article model
article_model = article_ns.model(
    'Article',
    {
        'id': fields.Integer(),
        'title': fields.String(),
        'author': fields.String(),
        'pub_date': fields.DateTime(),
        'source': fields.String(),
        'url': fields.String(),
    }
)


@article_ns.route('/articles')
class ArticleResource(Resource):
    @article_ns.marshal_with(article_model)
    @jwt_required()
    def get(self):
        """Get all articles"""
        articles = db.session.execute(db.select(Article)).scalars().all()

        return articles

    @article_ns.marshal_with(article_model)
    @article_ns.expect(article_model)
    @jwt_required()
    def post(self):
        """Create a new article"""
        data = request.get_json()

        new_article = Article(
            title=data['title'],
            author=data['author'],
            pub_date=datetime.fromisoformat(data['pub_date']),
            source=data['source'],
            url=data['url']
        )

        new_article.save()

        return new_article, 201
