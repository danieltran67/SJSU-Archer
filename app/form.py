from flask_login import login_user
from flask_wtf import FlaskForm
from werkzeug.routing import ValidationError
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email

from app.models import User, app


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Choose a valid email"), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Choose a different email.')


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
