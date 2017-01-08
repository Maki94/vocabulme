import os

from flask import flash
from flask import render_template

from services import *
from userServices import *


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

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    # session.init_app(app)
    app.debug = True
    app.run()
