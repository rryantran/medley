from exts import db

# user-feed association table
user_feed = db.Table('user_feed', db.Column('user_id', db.Integer, db.ForeignKey(
    'user.id')), db.Column('feed_id', db.Integer, db.ForeignKey('feed.id')))


# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    feeds = db.relationship('Feed', secondary=user_feed,
                            back_populates='users')

    def __repr__(self):
        return f'<User {self.username}>'

    def save(self):
        db.session.add(self)
        db.session.commit()


# feed model
class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(512), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_feed,
                            back_populates='feeds')
    articles = db.relationship(
        'Article', back_populates='feed', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Feed {self.title}>'

    def update(self, title, url):
        self.title = title
        self.url = url
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(512), unique=True, nullable=False)
    source = db.Column(db.String(128), nullable=False)
    feed = db.relationship('Feed', back_populates='articles')
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'), nullable=False)

    def __repr__(self):
        return f'<Article {self.title}>'
