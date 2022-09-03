from sqlalchemy import Integer, String, Text
from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id=db.Column(Integer, primary_key=True)
    name=db.Column(String)
    email=db.Column(String)
    password=db.Column(String)

    # challenges= owned by user


class Challenge(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    days=db.Column(Integer)

    # habits = habits included in it


class Habits(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String)
    completed=db.Column(Integer)

    # user=who owns it
