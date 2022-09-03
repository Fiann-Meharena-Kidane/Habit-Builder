from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from . import db

from .models import *

views = Blueprint('views', __name__)


@views.route('/home')
def home():
    challenge = Challenge.query.all()[0]
    challenge_name = challenge.name
    days = int(challenge.days)
    habits = [habit.name for habit in Habits.query.all()]

    # get challenge name, number of days, and list of habit names

    list_of_completed = [habit.completed.split('|')[:-1] for habit in Habits.query.all()]
    # list of completed days/ marked as done /

    for element in list_of_completed:
        for i in range(len(element)):
            if not (element[i]=='' or element[i]=='|'):
                element[i] = int(element[i])
                # make sure list of completed is does not contain elements other than int values

    return render_template('base.html', name=challenge_name, days=days, habits=habits, done=list_of_completed)


@views.route('/create', methods=['POST', 'GET'])
def create_challenge():
    # get name and days | create data entry | add entry
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
    # get habit name | create entry | add entry
    habit = request.form.get('habit')

    new_habit = Habits(
        name=habit,
        completed=''
    )

    db.session.add(new_habit)
    db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/completed/<habit>/<int:day>/')
def completed(day, habit):
    # get both habit name and day | update completed entry for that  habit and day
    habit = Habits.query.filter_by(name=habit).first()

    print(habit.completed)

    if not str(day) in habit.completed:
        habit.completed += str(day) + '|'
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/undo/<int:day>/<habit>')
def undo(habit, day):
    # get day and habit | update completed entry for that specific habit and day
    day = str(day)
    habit = Habits.query.filter_by(name=habit).first()

    updated_data = ''
    for value in habit.completed:
        if not day == value:
            updated_data += value
        final_data = updated_data[1:]

    print(final_data)

    habit.completed = final_data
    db.session.commit()

    return redirect(url_for('views.home'))
