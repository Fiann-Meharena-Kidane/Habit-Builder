import requests
from sqlalchemy import Integer, String, Text, ForeignKey
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    email = db.Column(String)
    password = db.Column(String)
    challenges = db.relationship('Challenge')
    # challenges= owned by user


class Challenge(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    days = db.Column(Integer)
    habits = db.relationship('Habits')
    user_id = db.Column(Integer, ForeignKey('user.id'))

    # habits = habits included in it


class Habits(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    completed = db.Column(Integer)
    percentile=db.Column(Integer)
    challenge_id = db.Column(Integer, ForeignKey('challenge.id'))

    # challenge_id is used to refer a given habit,


class Quotes(db.Model):
    id = db.Column(Integer, primary_key=True)
    quote = db.Column(String)
    author = db.Column(String)

    # table which contains quotes,


