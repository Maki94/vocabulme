import json
from functools import wraps

from flask import Flask, session

from classes import Word
from models.UserModel import UserModel
from models.WordModel import WordModel

app = Flask(__name__)


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
