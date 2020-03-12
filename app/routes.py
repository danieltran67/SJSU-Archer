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

db.create_all()

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
                return redirect(url_for('signup'))
        flash('Incorrect username/password. Try again.')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)
