from exts import db


# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


# feed model
class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(512), unique=True, nullable=False)

    def __repr__(self):
        return f'<Feed {self.title}>'


# article model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(512), unique=True, nullable=False)

    def __repr__(self):
        return f'<Article {self.title}>'
