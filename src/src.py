from services import *


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap


@app.route('/')
def home():
    try:
        session['logged_in'] = True
        flash("Hello from flash 1")
        flash("Hello from flash 2")
        return render_template('home.html')
    except Exception as e:
        print(e)
        return render_template('500.html')


# class RegistrationForm(Form):
#     email = StringField('username', [validators.length(min=4, max=20)])
#     password = PasswordField('New Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords must match')
#     ])
#     confirm = PasswordField('Repeat Password')
#     accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)',
#                               [validators.DataRequired()])


@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    # gc.collect()
    return redirect(url_for('dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    try:
        # form = RegistrationForm()
        # if request.method == "POST":
        #     email = form.email.data
        #     password = form.password.data
        #     hashedPassword = sha256_crypt.encrypt(password)
        #     # make connection
        #     # store
        #     # check if is valid, etc
        #     # if already taken: flash("Already taken") else insert into DB
        #
        #     flash("Thanks for registration :)")
        #     session['logged_in'] = True
        #     session['email'] = email
        #     return redirect(url_for('home'))
        # return render_template('register.html', form=form)
        return render_template('register.html')
    except Exception as e:
        return str(e)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    try:
        if request.method is "POST":
            attempted_email = request.form['email']
            attempted_password = request.form['password']
            if attempted_email is "admin@admin.com" and attempted_password is "admin":
                return redirect(url_for('logged'))
            else:
                error = "Invalid credentials. Try Again."
        elif request.method is "GET":
            return render_template('login.html')
        else:
            raise Exception("hello")
    except Exception as exception:
        print(exception)
        return render_template('500.html')


@app.route('/logged')
def logged():
    return render_template('logged.html')


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # session.init_app(app)

    app.debug = True
    app.run()
