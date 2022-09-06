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
            flash(f"Welcome, {current_user.name}!")
            return redirect(url_for('views.home'))
        else:
            flash(f"Email exists, login instead")
            return redirect(url_for('auth.login'))
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
                flash(f"Welcome, {current_user.name}!")
                return redirect(url_for('views.home'))
            else:
                flash('Password Incorrect', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Email does not exist, please register')
            return redirect(url_for('auth.register'))

    else:
        return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))