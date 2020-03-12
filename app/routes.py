from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_user, UserMixin
from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email
from app import db, app, form  # imported from init__
import secrets
import os
from werkzeug.urls import url_parse

from app.form import LoginForm, RegisterForm
from app.models import User

"""
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Choose a valid email"), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Choose a different email.')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique id per user info
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)

    # sets a encrypted password so no access through database
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

        # checks if passwords match

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
"""


@app.route('/')
def homePage():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user, remember=form.remember.data)
                flash('You were logged in')
                return redirect(url_for('dashboard'))
        flash('Incorrect username/password. Try again.')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = form.password.data
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)
