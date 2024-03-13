from exts import db


class FeedLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<FeedLink '{self.sourceName}', '{self.url}'>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, sourceName, url):
        self.sourceName = sourceName
        self.url = url
        db.session.commit()
