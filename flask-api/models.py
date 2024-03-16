from exts import db


# user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<User '{self.email}'>"


# feed link model
class FeedLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.Text(), nullable=False, unique=True)

    def __repr__(self):
        return f"<FeedLink '{self.name}', '{self.url}'>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, name, url):
        self.name = name
        self.url = url
        db.session.commit()
