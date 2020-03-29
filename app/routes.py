#from flask import render_template, flash, redirect, url_for, request
#from flask_login import login_user, login_required, logout_user, current_user
#from werkzeug.security import generate_password_hash
#from app import db, app
#from app.form import LoginForm, RegisterForm
#from app.models import User
from flask import render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email
from app import db, app, login_manager, form  # imported from init__
import secrets
import os
from werkzeug.urls import url_parse
from app.form import LoginForm, RegisterForm, SurveyForm, SurveyUpdateForm
from app.models import User, Survey


#db.create_all()

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
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))

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
        flash('You are now registered!')
        return redirect(url_for('login'))
    return render_template('signUp_Bootstrap.html', form=form, title="Register")


@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        option = Survey(major = form.major.data, outdoor = form.outdoor.data, indoor = form.indoor.data, user_id = current_user.id)
        db.session.add(option)
        db.session.commit()
        return redirect(url_for('user', username = current_user.username))

    return render_template('surveyBootstrap.html', form=form, title="Survey")

''' Changing survey needs to be worked on. it wont update'''
@app.route('/survey/updates', methods=['GET', 'POST'])
@login_required
def surveyUpdate():
    person = User.query.filter_by(username=current_user.username).first()
    userMajor = person.optionSurvey[0].major
    userOutdoor = person.optionSurvey[0].outdoor
    userIndoor = person.optionSurvey[0].indoor
    form = SurveyUpdateForm()
    if form.validate_on_submit():
        if form.major.data:
            userMajor=form.major.data
        if form.outdoor.data:
            userOutdoor=form.outdoor.data
        if form.indoor.data:
            userIndoor=form.indoor.data
        Survey(major = form.major.data, outdoor = form.outdoor.data, indoor = form.indoor.data, user_id = current_user.id)
        db.session.commit()
        flash("Activities Updated!")
        return redirect(url_for('user', username=current_user.username))
    return render_template('updateSurveyBootstrap.html', form = form, title ="Update Activities")


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('aboutUs.html', title="About Us")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contactUs.html')

@app.route('/profile/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    person = User.query.filter_by(username=current_user.username).first()
    userMajor = person.optionSurvey[0].major
    userOutdoor = person.optionSurvey[0].outdoor
    userIndoor = person.optionSurvey[0].indoor
    #userMajor = Survey.query.filter_by(major=major).first()
    #userOutdoor = Survey.query.filter_by(outdoor=outdoor).first()
    #userIndoor = survey.query.filter_by(indoor=indoor).first()

    return render_template('profile_Bootstrap.html', userMajor=userMajor, userOutdoor=userOutdoor, userIndoor=userIndoor)


@app.route('/profile/matches')
@login_required
def matches():
    return render_template('matches_Bootstrap.html', title = "Your Matches:")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('homePage'))
