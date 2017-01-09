import os
import json
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


def parse_json(data_list, success=True):
    try:
        return json.dumps({'data': data_list, 'success': success})
    except Exception as e:
        return str(e)


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
        words = WordModel().get_words(14)  # TODO: make heuristics
    else:
        words = WordModel().get_words(12)

    word_list = [word.get_dictionary() for word in words]
    return parse_json(word_list)


@app.route('/next_word', methods=['POST'])
@validate_json
def get_next_word():
    if 'logged_in' in session:
        words = WordModel().get_next_word()  # TODO: make heuristics
    else:
        words = WordModel().get_next_word()

    word_list = [word.get_dictionary() for word in words]
    return parse_json(word_list)


@app.route("/check_word/<word_name>/<word_definition>/<word_label>", methods=['POST'])
@validate_json
def check_word(word_name, word_definition, word_label):
    word_model = WordModel()
    state = word_model.is_matched(Word(name=word_name, definition=word_definition, label=word_label))
    print(state)
    if state:
        return parse_json("true")
    else:
        return parse_json("false")


@app.route('/twitter-example/<word_name>/<word_definition>/<word_label>', methods=['POST'])
@validate_json
def twitter_get_examples(word_name, word_definition, word_label):
    twitter_model = ExampleTwitterModel()
    examples = twitter_model.get_examples(Word(word_name, word_label, word_definition), 0, 5)
    return parse_json(examples.get_dictionary())


@app.route('/wikipedia-example/<word_name>/<word_definition>/<word_label>', methods=['POST'])
@validate_json
def wikipedia_get_examples(word_name, word_definition, word_label):
    wiki_model = ExampleWikipediaModel()
    examples = wiki_model.get_examples(Word(word_name, word_label, word_definition), 0, 4)
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

"""
    User procedures
"""


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap


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
