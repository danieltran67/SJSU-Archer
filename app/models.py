from app import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

'''
class to make data table.
'''


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


def init_db():
    db.create_all()
# create database. In case needed to remake database, delete current archer.db
# and run code below

# db.create_all()
# db.session.commit()
