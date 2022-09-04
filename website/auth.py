from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import *

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not User.query.filter_by(email=email).first():
            hashed_password=generate_password_hash(password, method='sha256')
            new_user = User(
                name=name,
                email=email,
                password=hashed_password
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            # return 'hello'
            return redirect(url_for('views.home'))
        else:
            return 'email exists, login'
    else:
        return render_template('register.html')


@auth.route('/', methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        user=User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password,request.form.get('password')):
                login_user(user)
                return redirect(url_for('views.home'))
            else:
                return 'wrong password'
        else:
            return 'email doesnt exist'

    else:
        return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')