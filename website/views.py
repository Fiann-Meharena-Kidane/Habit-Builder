from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user


views=Blueprint('views', __name__)


@views.route('/home')
def home():
    return render_template('base.html')


@views.route('/create', methods=['POST','GET'])
def create_challenge():
    name=request.form.get('name')
    days=int(request.form.get('days'))

    return render_template('base.html', table_title=name, days=days)


@views.route('/add-habit', methods=['POST', 'GET'])
def add_habit():
    habit=request.form.get('habit')

    return redirect(url_for('home'))
