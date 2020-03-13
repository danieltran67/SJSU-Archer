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
from app.form import LoginForm, RegisterForm
from app.models import User

#db.create_all()

@app.route('/')
def homePage():
    return render_template('landingPage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user', username = current_user.username))


    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password_hash:
                login_user(user, remember=form.remember.data)
                flash('You were logged in')
                return redirect(url_for('homePage'))
        flash('Incorrect username/password. Try again.')
    return render_template('login.html', form=form)

@app.route('/survey', methods=['GET', 'POST'])
@login_required
def surveyPage():
    return render_template('survey.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data,
                    password_hash=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template('profile.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homePage'))
