from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email
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


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
