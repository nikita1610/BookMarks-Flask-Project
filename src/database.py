import random
import string
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship('Bookmark',backref='user')

    def __repr__(self):
        return self.username
    

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_characters()
    
    def __repr__(self):
        return self.url
    
    def generate_short_characters(self):
        characters = string.digits + string.ascii_letters
        picked_chars = ''.join(random.choices(characters,k=3))
        link = self.query.filter_by(short_url=picked_chars).first()
        if link:
            self.generate_short_characters()
        return picked_chars
