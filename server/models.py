from exts import db

# article--user-feed association table
article_userfeed = db.Table('article_userfeed',
                            db.Column('article_id', db.Integer, db.ForeignKey(
                                'article.id'), primary_key=True),
                            db.Column('userfeed_id', db.Integer, db.ForeignKey(
                                'user_feed.id'), primary_key=True)
                            )


# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    feeds = db.relationship('UserFeed', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'


# feed model
class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), unique=True, nullable=False)
    users = db.relationship(
        'UserFeed', back_populates='feed')
    articles = db.relationship(
        'Article', back_populates='feed')

    def __repr__(self):
        return f'<Feed {self.url}>'


# user-feed model
class UserFeed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    user = db.relationship('User', back_populates='feeds')
    feed = db.relationship('Feed', back_populates='users')
    articles = db.relationship(
        'Article', secondary=article_userfeed, back_populates='userfeeds')

    def __repr__(self):
        return f'<UserFeed {self.title}>'


# article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(512), unique=True, nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)
    feed = db.relationship('Feed', back_populates='articles')
    userfeeds = db.relationship(
        'UserFeed', secondary=article_userfeed, back_populates='articles')

    def __repr__(self):
        return f'<Article {self.title}>'
