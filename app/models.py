from app import db


class User(db.Model):
    # dbModel  base class for database models provided by SQLalchamy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"User {self.username}"
