import os
import json
import threading
from concurrent.futures import thread
from functools import wraps

import pygal
from passlib.handlers.sha2_crypt import sha256_crypt
from flask import Flask, flash, redirect, render_template, request, session, url_for

from classes import User, Word
from models.ExampleTwitterModel import ExampleTwitterModel
from models.ExampleWikipediaModel import ExampleWikipediaModel
from models.UserModel import UserModel
from models.WordModel import WordModel

app = Flask(__name__)


@app.route('/hello')
def hello():
    return render_template('hello.html')


@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        print(e)
        return render_template('500.html')


# @app.errorhandler(404)
# def page_not_found():
#     return render_template('404.html')
#


def validate_json(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return parse_json([], False)

    return wrap


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first", "warning")
            return redirect(url_for('home'))

    return wrap


def parse_json(data_list, success=True):
    try:
        return json.dumps({'data': data_list, 'success': success})
    except Exception as e:
        print(e)
        return json.dumps({'data': [], 'success': False})


@app.route('/get_all_users', methods=['GET', 'POST', 'PUT', 'DELETE'])
@validate_json
def get_all_users():
    user_list = list()
    for user in UserModel().get_all():
        user_list.append(user.get_dictionary())

    return parse_json(user_list)


@app.route('/get_words', methods=['POST'])
@validate_json
def get_next_words():
    if 'logged_in' in session:
        words = WordModel().get_words(14)
    else:
        words = WordModel().get_words(12)

    word_list = [word.get_dictionary() for word in words]
    return parse_json(word_list)


@app.route('/next_word', methods=['POST'])
@validate_json
def get_next_word():
    if 'logged_in' in session:
        logged_user = User(email=session['logged_in'])
        word_view_list = UserModel().get_recommended_model_list(logged_user)
    else:
        word_view_list = UserModel().get_recommended_model_list()

    words = [word.word for word in word_view_list]

    t_twitter = threading.Thread(target=ExampleTwitterModel.trigger_database, args=(words, 0, 5))
    t_wikipedia = threading.Thread(target=ExampleWikipediaModel.trigger_database, args=(words, 0, 2))
    t_twitter.start()
    t_wikipedia.start()

    model_list = [word_model.get_dictionary() for word_model in word_view_list]
    return parse_json(model_list)


@app.route("/check_word/<word_name>/<word_definition>/<word_label>", methods=['POST'])
@validate_json
def check_word(word_name, word_definition, word_label):
    word_model = WordModel()
    state = word_model.is_matched(Word(name=word_name, definition=word_definition, label=word_label))
    print(state)
    if state:
        return parse_json(True)
    else:
        return parse_json(False)


@app.route('/twitter-example/<word_name>/<word_definition>/<word_label>', methods=['POST'])
@validate_json
def twitter_get_examples(word_name, word_definition, word_label):
    twitter_model = ExampleTwitterModel()
    examples = twitter_model.get_examples(Word(word_name, word_label, word_definition), 0, 5)
    return parse_json(examples.get_dictionary())


@app.route('/seen-word/<word_name>/<word_definition>/<word_label>/<int:correct>', methods=['POST'])
@validate_json
def seen_word(word_name: str, word_definition: str, word_label: str, correct: int):
    """
        correct: 0 => incorrect
        correct: 1 => correct
    """
    if 'logged_in' in session:
        if 'email' in session:
            email = session['email']
            userModel = UserModel()
            if correct == 0:
                userModel.seen_word(user=User(email), word=Word(word_name, word_label, word_definition), correct=False)
            elif correct == 1:
                userModel.seen_word(user=User(email), word=Word(word_name, word_label, word_definition), correct=True)
            else:
                raise Exception("Invalid correct argument, function seen_word")
            return parse_json(True)
        else:
            print(session['logged_in'])
    else:
        return parse_json(False)


@app.route('/wikipedia-example/<word_name>/<word_definition>/<word_label>', methods=['POST'])
@validate_json
def wikipedia_get_examples(word_name, word_definition, word_label):
    wiki_model = ExampleWikipediaModel()
    examples = wiki_model.get_examples(Word(word_name, word_label, word_definition), 0, 2)
    return parse_json(examples)


@app.route('/graph', methods=['GET'])
def graph():
    graph_pygal = pygal.Line()
    graph_pygal.title = '% Change Coolness of programming languages over time.'
    graph_pygal.x_labels = ['2011', '2012', '2013', '2014', '2015', '2016']
    graph_pygal.add('Python', [15, 31, 89, 200, 356, 900])
    graph_pygal.add('Java', [15, 45, 76, 80, 91, 95])
    graph_pygal.add('C++', [5, 51, 54, 102, 150, 201])
    graph_pygal.add('All others combined!', [5, 15, 21, 55, 92, 105])

    graph_data = graph_pygal.render_data_uri()
    return render_template('graph.html', graph_data=graph_data)


@app.route('/finished', methods=['GET'])
@login_required
def finished_round():

    user = User(session['email'])
    user_model = UserModel()
    word_list_view = user_model.get_word_list_view(user)
    seen_list = word_list_view.seen_word_list
    learnt_list = word_list_view.learnt_word_list
    forgotten_list = word_list_view.forgotten_word_list

    # graph_pygal = pygal.Line()
    # graph_pygal.title = '% Change Coolness of programming languages over time.'
    # graph_pygal.x_labels = ['2011', '2012', '2013', '2014', '2015', '2016']
    # graph_pygal.add('Python', [15, 31, 89, 200, 356, 900])
    # graph_pygal.add('Java', [15, 45, 76, 80, 91, 95])
    # graph_pygal.add('C++', [5, 51, 54, 102, 150, 201])
    # graph_pygal.add('All others combined!', [5, 15, 21, 55, 92, 105])

    pie_chart = pygal.Pie()
    pie_chart.title = 'TITLE'
    pie_chart.add('Seen Words', WordModel.get_number_labels(seen_list))
    pie_chart.add('Forgotten Words', WordModel.get_number_labels(forgotten_list))
    pie_chart.add('Learnt Words', WordModel.get_number_labels(learnt_list))
    pie_chart.render()
    graph_data = pie_chart.render_data_uri()

    return render_template('list.html',
                           seen_list=seen_list,
                           learnt_list=learnt_list,
                           forgotten_list=forgotten_list,
                           graph_data=graph_data
                           )


"""
    User procedures
"""


@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    flash('Successfully logged out', 'success')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    try:
        if request.method == "POST":
            email = request.form['email']
            password = sha256_crypt.encrypt(request.form['password'])

            userModel = UserModel()

            if userModel.get(User(email=email)):
                flash("User already exist", 'warning')
            else:
                userModel.create(User(email, password))

                session['logged_in'] = True
                session['email'] = email

                flash("Thanks for registration :)", 'success')
    except Exception as e:
        print(e)
        flash("Database error", 'warning')
    else:
        return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            userModel = UserModel()

            if userModel.is_valid(User(email, password)):
                hashed_password = userModel.get(User(email)).password
                if sha256_crypt.verify(password, hashed_password):
                    flash("Successfully logged!", 'success')
                    session['logged_in'] = True
                    session['email'] = email
                else:
                    flash("Wrong credentials!", 'warning')
            else:
                flash("Invalid credentials. Try Again.", 'warning')
    except Exception as exception:
        flash('Database error', 'warning')
        print(exception)
    finally:
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    # session.init_app(app)
    app.debug = True
    app.run()
