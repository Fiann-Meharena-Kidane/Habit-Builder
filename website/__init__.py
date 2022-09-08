import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
db = SQLAlchemy()
DB_NAME = 'challenges.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Quotes

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_managers=LoginManager()
    login_managers.login_view='auth.login'
    login_managers.init_app(app)

    @login_managers.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

