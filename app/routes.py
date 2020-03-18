from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from app import db, app
from app.form import LoginForm, RegisterForm, SurveyForm
from app.models import User, Survey

db.create_all()

"""
NOTE: This python file does NOT run the website. That is archer.py
__init__.py, form.py, models.py, and routes.py are all files that make the website function! 
This python file is how website navigates thru different links such as /login, /signup, etc.
The sign up and sign in uses a package called FlaskForm, found in forms.py,  that saves our username/password into 
a database called db.sqlite3.
The database is created via sqlite3 and the coed is found in models.py.

"""


@app.route('/')
def homePage():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user, remember=form.remember.data)
                flash('You were logged in')
                return redirect(url_for('survey'))
        flash('Incorrect username/password. Try again.')
    return render_template('login_Bootstrap.html', form=form, title="Login")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        flash('Already taken. Try again.')
    return render_template('signUp_Bootstrap.html', form=form, title="Register")


@app.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()

    if form.validate_on_submit():
        option = Survey(major=form.major.data, outdoor=form.outdoor.data, indoor=form.indoor.data)
        db.session.add(option)
        db.session.commit()
        return redirect(url_for('about'))
    return render_template('surveyBootstrap.html', form=form, title="Survey")


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('aboutUs.html', title="About Us")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contactUs.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))





