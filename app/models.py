from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    auth_level = db.Column(db.Integer, nullable=False)

class Tab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    url = db.Column(db.String(25), nullable=False)
    req_auth_level = db.Column(db.Integer, default=1, nullable=False)
    data = db.relationship("accData", backref="tab", lazy="dynamic")

class accData(db.Model):
    def __repr__(self):
        return str({"id": self.id, "title": self.title, "text": self.text})
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)
    text = db.Column(db.String(1500))
    tabid = db.Column(db.Integer, db.ForeignKey("tab.id"))
    