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

    def __repr__(self):
        return f'<user: {self.username}>, <password: {self.password}>, <email: {self.email}>'

# create database. In case needed to remake database, delete current archer.db
# and run code below

# db.create_all()
# db.session.commit()
