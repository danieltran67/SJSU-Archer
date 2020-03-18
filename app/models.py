from app import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

'''
class to make data table.
'''


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique id per user info
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(128), index=True, unique=True)
    optionSurvey = db.relationship('Survey', backref='author', lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return "User(username='{self.username}', " \
                "email='{self.email}', " \
               "password='{self.password}')".format(self=self)


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    major = db.Column(db.String(100))
    outdoor = db.Column(db.String(100))
    indoor = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, major, outdoor, indoor):
        self.major = major
        self.outdoor = outdoor
        self.indoor = indoor

    def __repr__(self):
        return "User(major='{self.major}', " \
               "outdoor='{self.outdoor}', " \
               "indoor='{self.indoor}', " \
               "user_id='{self.user_id}')".format(self=self)

# create database. In case needed to remake database, delete current archer.db
# and run code below

# db.create_all()
# db.session.commit()
#.quit
