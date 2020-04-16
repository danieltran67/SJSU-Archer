from app import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


'''
class to make data table.
'''


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

friendsList = db.Table('friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), index = True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique id per user info
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(128), index=True, unique=True)
    surveyVisted = db.Column(db.Boolean)
    optionSurvey = db.relationship('Survey', backref = "person", lazy = 'dynamic')
    friends = db.relationship('User', secondary = friendsList,
                            primaryjoin=id==friendsList.c.user_id,
                            secondaryjoin=id==friendsList.c.friend_id,
                            backref = db.backref('friendsList', lazy = 'dynamic'),
                            lazy = 'dynamic')


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def befriend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            return self
    def unfriend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            return self

    def isFriendsWith(self, friend):
        return self.friends.filter(friend.c.friend_id == user.id)

    def __repr__(self):
        return "User(username='{self.username}', " \
                "email='{self.email}', " \
               "password='{self.password}')".format(self=self)
'''
class Request(db.Model):
    id = db.Column(db.Integer, primary_key = True)

class userRelation(db.Model):
    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key = True)
    request_from_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key = True)
    request_id = db.Column(db.Integer, ForeignKey('request.id'))

    approved = db.Column(db.Boolean, default = False)

    user = db.relationship('User', foreign_keys[id], uselist = False)
    request_from = db.relationship('User', foreign_keys=[request_from_id], uselist = False)
    request = db.relationship('Request', uselist=False, cascade='all, delete-orphan', single_parent = True)
'''
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    major = db.Column(db.String(100))
    outdoor = db.Column(db.String(100))
    indoor = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, major, outdoor, indoor, user_id):
        self.major = major
        self.outdoor = outdoor
        self.indoor = indoor
        self.user_id = user_id

    def __repr__(self):
        return "User(major='{self.major}', " \
               "outdoor='{self.outdoor}', " \
               "indoor='{self.indoor}', " \
               "user_id='{self.user_id}')".format(self=self)

'''
class interests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interests = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #links choices to user

    def __init__(self, interests):
        self.interests = interests

    def __repr__(self):
        return "User(interests = '{self.interests}')".format(self=self)

class majors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    majors = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #links choices to user


    '''

# create database. In case needed to remake database, delete current archer.db
# and run code below

#db.create_all()
#db.session.commit()
