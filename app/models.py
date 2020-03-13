from app import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

'''
class to make data table.
'''




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique id per user info
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(80))
    email = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return f'<user: {self.username}>, <password: {self.password_hash}>, <email: {self.email}>'

    def set_pass(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class interests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String())
    uid = db.Column(db.Integer, db.ForeignKey('user.id')) #links choices to user

@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# create database. In case needed to remake database, delete current db.sqlite3
# and run code below

#db.create_all()
#db.session.commit()
