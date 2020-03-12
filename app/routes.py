from flask import render_template, flash, redirect, url_for, session, request
from app import db, app  # imported from init__
import secrets
import os
from werkzeug.urls import url_parse
from app.models import User


@app.route('/')
def homePage():
    return render_template('signUpLogin.html')


@app.route('/login')
def login():
    return render_template('login.html')
