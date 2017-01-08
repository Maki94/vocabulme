from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from passlib.handlers.sha2_crypt import sha256_crypt

from services import *
from classes import User


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
        return redirect('home')


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
