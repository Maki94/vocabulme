import json
from functools import wraps

from flask import Flask, session

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


@app.route('/get_words', methods=['GET', 'POST'])
@validate_json
def get_next_words():
    if 'logged_in' in session:
        words = WordModel().get_words(14)  # TODO: make heuristics
    else:
        words = WordModel().get_words(12)  # TODO: return random words

    word_list = list()
    for word in words:
        word_list.append(word.get_dictionary())

    return parse_json(word_list)
