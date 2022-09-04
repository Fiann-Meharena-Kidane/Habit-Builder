from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
from . import db

from .models import *

views = Blueprint('views', __name__)


@views.route('/home')
def home():
    try:
        # challenge = Challenge.query.all()[0]
        challenge=Challenge.query.filter_by(user_id=current_user.id)[0]
    except IndexError:
        return render_template('base.html')
        # if no challenge found render base,
    else:
        challenge=Challenge.query.filter_by(user_id=current_user.id)[0]

    challenge_name = challenge.name
    days = int(challenge.days)
    habits = [habit.name for habit in challenge.habits]
    # get all habits for this specific challenge,
    all_challenges = Challenge.query.filter_by(user_id=current_user.id).all()
    # to be displayed on the drop-down menu,

    # gets challenge name, number of days, and list of habit names

    list_of_completed = [habit.completed.split('|')[:-1] for habit in Habits.query.filter_by(challenge_id=challenge.id)]
    # list_of_completed = [habit.completed.split('|')[:-1] for habit in habits]
    # list of completed days/ marked as done /

    for element in list_of_completed:
        for i in range(len(element)):
            if not (element[i]=='' or element[i]=='|'):
                element[i] = int(element[i])
                # make sure list of completed is does not contain elements other than int values

    return render_template('base.html',
                           current_user=current_user,
                           name=challenge_name,
                           days=days,
                           habits=habits,
                           done=list_of_completed,
                           challenges=all_challenges)


@views.route('/show-challenge/<challenge>', methods=['POST','GET'])
def show_challenge(challenge):

    # details about challenge, habit and completed ones
    target_challenge=Challenge.query.filter_by(name=challenge).first()
    habits = [habit.name for habit in target_challenge.habits]
    all_challenges = Challenge.query.filter_by(user_id=current_user.id).all()
    list_of_completed = [habit.completed.split('|')[:-1] for habit in Habits.query.filter_by(challenge_id=target_challenge.id)]

    for element in list_of_completed:
        for i in range(len(element)):
            if not (element[i]=='' or element[i]=='|'):
                element[i] = int(element[i])

    return render_template('base.html',
                           current_user=current_user,
                           name=target_challenge.name,
                           days=int(target_challenge.days),
                           habits=habits,
                           done=list_of_completed,
                           challenges=all_challenges)
    # render the requested challenge,


@views.route('/create', methods=['POST', 'GET'])
def create_challenge():
    # get name and days | create data entry | add entry
    name = request.form.get('name')
    days = int(request.form.get('days'))

    new_challenge = Challenge(
        name=name,
        days=days,
        user_id=current_user.id
    )

    db.session.add(new_challenge)
    db.session.commit()

    return redirect(url_for('views.show_challenge', challenge=name))


@views.route('/add-habit/<challenge_name>', methods=['POST', 'GET'])
def add_habit(challenge_name):
    # get habit name | create entry | add entry
    habit = request.form.get('habit')
    current_challenge=Challenge.query.filter_by(name=challenge_name).first()
    new_habit = Habits(
        name=habit,
        completed='',
        challenge_id=current_challenge.id
    )

    db.session.add(new_habit)
    db.session.commit()
    #
    return redirect(url_for('views.show_challenge',challenge=challenge_name))


@views.route('/completed/<habit>/<int:day>/<challenge>')
def completed(day, habit,challenge):
    # get both habit name and day | update completed entry for that  habit and day
    habit = Habits.query.filter_by(name=habit).first()

    print(habit.completed)

    if not str(day) in habit.completed:
        habit.completed += str(day) + '|'
        db.session.commit()

    return redirect(url_for('views.show_challenge', challenge=challenge))


@views.route('/undo/<int:day>/<habit>/<challenge>')
def undo(habit, day, challenge):
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

    return redirect(url_for('views.show_challenge', challenge=challenge))


@views.route('/delete-challenge/<challenge>', methods=['POST','GET'])
def delete_challenge(challenge):
    target_challenge=Challenge.query.filter_by(name=challenge).first()

    db.session.delete(target_challenge)
    db.session.commit()

    return redirect(url_for('views.home'))