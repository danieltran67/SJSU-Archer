from flask_login import login_user
from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email
from app import Bootstrap
from app.models import User, app


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please use a different name.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email taken. Please use a different email.')

class SurveyForm(FlaskForm):
    major = SelectField(u'Major', choices=[('cmpe', 'Computer Engineering'),
                                           ('cs', "Computer Science"),
                                           ('se', 'Software Engineering')])
    outdoor = SelectField(u'Outdoor Activities', choices=[('rave', 'Concerts'),
                                           ('eat', "Going Out to Eat"),
                                           ('gym', 'Gym'),
                                           ('sports', 'Sports')])
    indoor = SelectField(u'Indoor Activities', choices=[('game', 'Video Games'),
                                           ('books', "Reading"),
                                           ('music', 'Playing Music')])


class SurveyUpdateForm(FlaskForm):
    major = SelectField(u'Major', choices=[('cmpe', 'Computer Engineering'),
                                           ('cs', "Computer Science"),
                                           ('se', 'Software Engineering')])
    outdoor = SelectField(u'Outdoor Activities', choices=[('rave', 'Concerts'),
                                           ('eat', "Going Out to Eat"),
                                           ('gym', 'Gym'),
                                           ('sports', 'Sports')])
    indoor = SelectField(u'Indoor Activities', choices=[('game', 'Video Games'),
                                           ('books', "Reading"),
                                           ('music', 'Playing Music')])
'''
    def __init__(self, oldData, *arg, **kwargs):
        super(SurveyUpdateForm, self).__init__(*arg, **kwargs)
        self.oldData = oldData
'''

@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
