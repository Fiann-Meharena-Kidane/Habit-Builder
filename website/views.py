from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from . import db

from .models import *

views = Blueprint('views', __name__)


@views.route('/home')
def home():
    challenge = Challenge.query.all()[0]
    name = challenge.name
    days = int(challenge.days)
    habits = [habit.name for habit in Habits.query.all()]

    list_of_completed = [habit.completed.split('|')[:-1] for habit in Habits.query.all()]
    for element in list_of_completed:
        for i in range(len(element)):
            element[i] = int(element[i])

    return render_template('base.html', name=name, days=days, habits=habits, done=list_of_completed)


@views.route('/create', methods=['POST', 'GET'])
def create_challenge():
    name = request.form.get('name')
    days = int(request.form.get('days'))

    new_challenge = Challenge(
        name=name,
        days=days
    )

    db.session.add(new_challenge)
    db.session.commit()

    return render_template('base.html', table_title=name, days=int(days))


@views.route('/add-habit', methods=['POST', 'GET'])
def add_habit():
    habit = request.form.get('habit')

    new_habit = Habits(
        name=habit,
        completed=''
    )

    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/completed/<int:day>/<habit>')
def completed(day, habit):


    habit = Habits.query.filter_by(name=habit).first()

    if not str(day) in habit.completed:
        habit.completed += str(day) + '|'
    db.session.commit()

    return redirect(url_for('views.home'))
