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
    interests = db.relationship('interests', backref="author", lazy='dynamic')
    majors = db.relationship('majors', backref="author",lazy='dynamic')

    def __repr__(self):
        return f'<user: {self.username}>, <password: {self.password}>, <email: {self.email}>'

class interests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interests = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #links choices to user

class majors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    majors = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #links choices to user

# create database. In case needed to remake database, delete current archer.db
# and run code below

db.create_all()
db.session.commit()
