import flask_login
import requests
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
import datetime
now=datetime.datetime.now()
from .models import *
from quickchart import QuickChart


qc = QuickChart()
# qc.width = 200
# qc.height = 150

views = Blueprint('views', __name__)


@views.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        quotes=Quotes.query.all()
        year=now.year
        try:
            # challenge = Challenge.query.all()[0]
            challenge = Challenge.query.filter_by(user_id=current_user.id)[0]
        except IndexError:
            return render_template('base.html')
            # if no challenge found render base,
        else:
            challenge = Challenge.query.filter_by(user_id=current_user.id)[0]

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
                if not (element[i] == '' or element[i] == '|'):
                    element[i] = int(element[i])
        # make sure list of completed is does not contain elements other than int values

        print(list_of_completed)

        list_of_guages=[int(len(habit)/7*100) for habit in list_of_completed]
        config_1 = """{type: 'radialGauge',data: { datasets: [{ data: [ """
        config_2 = """], backgroundColor: getGradientFillHelper('horizontal', ['red', 'blue']),  }]  },
          options: { // See https://github.com/pandameister/chartjs-chart-radial-gauge#options    domain: [0, 100],
            trackColor: '#f0f8ff', centerPercentage: 90, centerArea: {  text: (val) => val + '%', },}
        }"""
        number = '0'
        list_of_images=[]
        for gauge in list_of_guages:
            number=gauge
            qc.config = f"{config_1}{number}{config_2}"
            image_url = qc.get_url()
            list_of_images.append(image_url)


        return render_template('base.html',
                               current_user=current_user,
                               name=challenge_name,
                               days=days,
                               habits=habits,
                               done=list_of_completed,
                               challenges=all_challenges,
                               quotes=quotes,
                               year=year,
                               images=list_of_images)
    else:
        return 'not logged in'


@views.route('/show-challenge/<challenge>', methods=['POST', 'GET'])
@login_required
def show_challenge(challenge):
    quotes = Quotes.query.all()
    year=now.year
    # details about challenge, habit and completed ones
    target_challenge = Challenge.query.filter_by(name=challenge).first()
    # print(target_challenge.name)

    habits = [habit.name for habit in target_challenge.habits]
    print(habits)
    all_challenges = Challenge.query.filter_by(user_id=current_user.id).all()
    print(all_challenges)
    list_of_completed = [habit.completed.split('|')[:-1] for habit in
                         Habits.query.filter_by(challenge_id=target_challenge.id)]

    for element in list_of_completed:
        for i in range(len(element)):
            if not (element[i] == '' or element[i] == '|'):
                element[i] = int(element[i])
    print(list_of_completed)

    # API call to draw a gauge chart

    list_of_gauges = [int(len(habit) / target_challenge.days * 100) for habit in list_of_completed]
    config_1 = """{type: 'radialGauge',data: { datasets: [{ data: [ """
    config_2 = """], backgroundColor: getGradientFillHelper('horizontal', ['red', 'blue']),  }]  },
      options: { // See https://github.com/pandameister/chartjs-chart-radial-gauge#options    domain: [0, 100],
        trackColor: '#f0f8ff', centerPercentage: 90, centerArea: {  text: (val) => val + '%', },}
    }"""
    number = '0'
    list_of_images = []
    for gauge in list_of_gauges:
        number = gauge
        qc.config = f"{config_1}{number}{config_2}"
        image_url = qc.get_url()
        list_of_images.append(image_url)
    # creates list of gauges

    return render_template('base.html',
                           current_user=current_user,
                           name=target_challenge.name,
                           days=int(target_challenge.days),
                           habits=habits,
                           done=list_of_completed,
                           challenges=all_challenges,
                           quotes=quotes,
                           year=year,
                           images=list_of_images)
    # render the requested challenge,


@views.route('/create', methods=['POST', 'GET'])
def create_challenge():
    # get name and days | create data entry | add entry
    name = request.form.get('name')
    days = 7

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
    current_challenge = Challenge.query.filter_by(name=challenge_name).first()
    new_habit = Habits(
        name=habit,
        completed='',
        challenge_id=current_challenge.id
    )

    db.session.add(new_habit)
    db.session.commit()
    #
    return redirect(url_for('views.show_challenge', challenge=challenge_name))


@views.route('/completed/<habit>/<int:day>/<challenge>')
def completed(day, habit, challenge):
    # get both habit name and day | update completed entry for that  habit and day
    habit = Habits.query.filter_by(name=habit).first()

    current_completed = habit.completed
    if not str(day) in current_completed:
        current_completed += f"{day}|"
        # add a marker

    habit.completed = current_completed
    db.session.commit()

    return redirect(url_for('views.show_challenge', challenge=challenge))


@views.route('/undo/<int:day>/<habit>/<challenge>')
def undo(habit, day, challenge):
    # get day and habit | update completed entry for that specific habit and day
    day = str(day)
    habit = Habits.query.filter_by(name=habit).first()

    current_completed = habit.completed
    final_completed = current_completed.replace(f"{day}|", '')
    # replace/ remove day value

    habit.completed = final_completed
    db.session.commit()

    return redirect(url_for('views.show_challenge', challenge=challenge))


@views.route('/delete-challenge/<challenge>', methods=['POST', 'GET'])
def delete_challenge(challenge):
    target_challenge = Challenge.query.filter_by(name=challenge).first()

    db.session.delete(target_challenge)
    db.session.commit()

    return redirect(url_for('views.home'))


@views.route('/<habit>/<challenge>')
def delete_habit(habit, challenge):
    target_challenge=Challenge.query.filter_by(name=challenge).first()
    all_habits=target_challenge.habits
    # list of habits under the challenge on target,

    for entry in all_habits:
        if entry.name==habit:
            # find the habit in the challenge , and delete it,
            target_habit=Habits.query.filter_by(name=entry.name).first()
            db.session.delete(target_habit)
            db.session.commit()
            return redirect(url_for('views.show_challenge', challenge=challenge))

    # for habit in all_habits:


@views.route('/stat/<challenge>')
def stat(challenge):
    target_challenge=Challenge.query.filter_by(name=challenge).first()
    days=target_challenge.days
    habit_objects=target_challenge.habits
    habits=[habit.name for habit in habit_objects]
    completed_ones=[entry.completed.split('|')[:-1] for entry in habit_objects]

    efficiency=[] # holds list of percentiles

    for value in range(1,11):  # calculates the the rate of completion in each day,
        count=0
        for entry in completed_ones:
            if str(value) in entry:
                count+=1
        efficiency.append(count)

    gauges=[int(len(data)/days*100)for data in completed_ones]
    days_low=[f"DAY - {day}" for day in range(1, days+1)]

    bar_chart=QuickChart()

    # draw bar chart,
    configure = {
        'type': 'bar',
        'data':
            {
                'labels': days_low,
                'datasets': [

        {
            'label': 'Efficiency',
            'data':efficiency,
            'backgroundColor': '#37ed7d'
        }

    ]

            }
    }
    bar_chart.config=configure
    image_source=bar_chart.get_short_url()

    return render_template('base.html', challenge=challenge, image_source=image_source)


@views.route('/fill')
def fill():
    response = requests.get('https://zenquotes.io/api/quotes')
    quotes = response.json()

    if not Quotes.query.all():
        for entry in quotes:
            quote = entry['q']
            author = entry['a']

            new_quote = Quotes(
                quote=quote,
                author=author
            )

            db.session.add(new_quote)
            db.session.commit()

    return f"DB Population Successful!"
