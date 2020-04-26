import pickle
import sqlite3
import sys
from aifc import Error

from datetime import datetime

from flask import render_template, flash, redirect, url_for, session, request
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from app import db, app, login_manager, form, yagmail, yag  # imported from init__,
from app.form import LoginForm, RegisterForm, SurveyForm, SurveyUpdateForm, \
    MessageForm, RequestResetForm, ResetPasswordForm, ReportForm
from app.models import User, Survey, Message, Serializer, Report
from datetime import datetime
import array as arr

"""
NOTE: This python file does NOT run the website. That is archer.py
__init__.py, form.py, models.py, and routes.py are all files that make the website function!
This python file is how website navigates thru different links such as /login, /signup, etc.
The sign up and sign in uses a package called FlaskForm, found in forms.py,  that saves our username/password into
a database called db.sqlite3.
The database is created via sqlite3 and the coed is found in models.py.

"""


@app.route('/')
def homePage():
    return render_template('home.html')


### ----LOGIN/REGISTRATION CODE ---------------------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user, remember=form.remember.data)
                flash('You were logged in')
                if user.surveyVisted == 1:
                    return redirect(url_for('user', username=current_user.username))
                else:
                    return redirect(url_for('survey'))
        flash('Incorrect username/password. Try again.')
    return render_template('login_Bootstrap.html', form=form, title="Login")


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent to reset your password')
            return redirect(url_for('login'))
    return render_template('reset_request_Bootstrap.html', title='Reset Password', form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    body = f"Archer Password Reset Link: " \
           f"{url_for('reset_token', token=token, _external=True)}"
    receiver = user.email
    yag.send(to=receiver,
             subject="SJSU Archer Reset Password",
             contents=body)


# Required for reset_request to match user
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    user = User.verify_reset_token(token)
    if user is None:  # If the token is wrong or expired
        flash('That is an invalid  or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = form.password.data
        user.password = hashed_password
        db.session.commit()
        flash('Your password updated!')
        return redirect(url_for('homePage'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, studentName=form.studentName.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('You are now registered!')
        return redirect(url_for('login'))
    return render_template('signUp_Bootstrap.html', form=form, title="Register")


### ----LOGIN/REGISTRATION CODE  END---------------------------------------------------------------------------------------

### ----SURVEY CODE ---------------------------------------------------------------------------------------
@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    visit = User.query.filter_by(username=current_user.username).first()
    visit.surveyVisted = 1
    form = SurveyForm()
    if form.validate_on_submit():
        option = Survey(major=form.major.data, outdoor=form.outdoor.data, indoor=form.indoor.data,
                        user_id=current_user.id)
        db.session.add(option)
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))

    return render_template('surveyBootstrap.html', form=form, title="Survey")


@app.route('/survey/updates', methods=['GET', 'POST'])
@login_required
def surveyUpdate():
    personSurvey = Survey.query.filter_by(
        user_id=current_user.id).first()  # finds data connection between survey and user
    form = SurveyUpdateForm()
    if form.validate_on_submit():
        if form.major.data:
            personSurvey.major = form.major.data
        if form.outdoor.data:
            personSurvey.outdoor = form.outdoor.data
        if form.indoor.data:
            personSurvey.indoor = form.indoor.data
        Survey(major=form.major.data, outdoor=form.outdoor.data, indoor=form.indoor.data, user_id=current_user.id)
        db.session.commit()
        flash("Activities Updated!")
        return redirect(url_for('user', username=current_user.username))
    return render_template('updateSurveyBootstrap.html', form=form, title="Update Activities")


### ----SURVEY CODE  END---------------------------------------------------------------------------------------

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('aboutUs.html', title="About Us")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('ContactUs_Bootstrap.html')


### ----PROFILE CODE  ---------------------------------------------------------------------------------------
@app.route('/profile/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.surveyVisted == 1:
        personSurvey = Survey.query.filter_by(user_id=current_user.id).first()
    else:
        return redirect(url_for('survey'))
    return render_template('profile_Bootstrap.html', userMajor=personSurvey.major, userOutdoor=personSurvey.outdoor,
                           userIndoor=personSurvey.indoor)


@app.route('/profile/user_page/<username>') # This is the dashboard
@login_required
def userProfile(username):
    user = User.query.filter_by(username=username).first_or_404()
    personSurvey = Survey.query.filter_by(user_id=user.id).first()
    return render_template('accountProfile_Bootstrap.html', userMajor=personSurvey.major,
                           userOutdoor=personSurvey.outdoor, userIndoor=personSurvey.indoor, user=user)


@app.route('/profile/user_page/<username>')
@login_required
def friendProfile(username):
    user = User.query.filter_by(username=username).first_or_404()
    personSurvey = Survey.query.filter_by(user_id=user.id).first()
    return render_template('accountProfile_Bootstrap.html', userMajor=personSurvey.major,
                           userOutdoor=personSurvey.outdoor, userIndoor=personSurvey.indoor, user=user)


### ----PROFILE CODE  END---------------------------------------------------------------------------------------
### ----REPORT PROFILE CODE ------------------------------------------------------------------------------------
@app.route('/profile/user_page/<username>/report', methods=["GET", "POST"])
def reportUser(username):
    user = User.query.filter_by(username=username).first()
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(reasonReported=form.reasons.data, report_recipient_id = user.id)
        db.session.add(report)
        db.session.commit()
        send_warning_email(username)
        flash('User has been Reported!')
        return redirect(url_for('friendProfile', username=username))
    return render_template('reportUser_Bootstrap.html', user = user, form=form)

def send_warning_email(username):
    #find person ID
    user = User.query.filter_by(username = username).first()
    #find person being reported
    personReported = Report.query.filter_by(report_recipient_id = user.id).order_by(Report.id.desc()).first()
    body = f"You have been reported for: " \
           f"{personReported.reasonReported}" \
           f"Please reflect on your behavior before actions are taken"
    receiver = user.email
    yag.send(to=receiver,
             subject="Archer account warning",
             contents=body)



### ----REPORT PROFILE CODE END ------------------------------------------------------------------------------------
### ----CHAT CODE ---------------------------------------------------------------------------------------
@app.route('/direct_message', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('chat_Bootstrap.html')


@app.route('/message/<username>', methods=['GET', 'POST'])
@login_required
def sendMsg(username):
    user = User.query.filter_by(username=username).first_or_404()
    messages = current_user.messageRecieved.order_by(Message.timestamp.desc())
    chatLog = main(current_user.id, user.id)
    form = MessageForm()

    if form.validate_on_submit():
        msg = Message(sender_id=current_user.id, recipient_id=user.id, body=form.message.data)

        db.session.add(msg)
        db.session.commit()

        flash('Message Sent')

        chatLog = main(current_user.id, user.id)
        i = 0
        return redirect(url_for('sendMsg', username=username, ))
    return render_template('sendMsg_Bootstrap.html', title='Messaging',
                           form=form, user=user,
                           messages=messages, chatLog=chatLog, len=len(chatLog),
                           current_user=current_user)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_task_by_priority(conn, recipient_id,
                            sender_id, ):  # Tasks by priority and fetches all that matches that priority
    cur = conn.cursor()

    # Gets all of sender's/receiver's text
    cur.execute("SELECT DISTINCT * FROM message as one "
                "INNER JOIN user as two "
                "ON "
                "(((one.sender_id=? AND one.recipient_id=?) "
                "OR (one.sender_id=? AND one.recipient_id=?)))"
                "OR (two.id = one.recipient_id OR two.id = one.sender_id) "
                "GROUP BY one.timestamp, two.username "
                "HAVING two.id = one.recipient_id OR two.id = one.sender_id",
                (sender_id, recipient_id, recipient_id, sender_id,))
    '''
    cur.execute("SELECT sender_id, recipient_id FROM message as one "
                "INTERSECT "
                "SELECT recipient_id, sender_id FROM message as two "
                "GROUP BY one.timestamp, two.username "
                "HAVING two.id = one.recipient_id OR two.id = one.sender_id")
                '''

    rows = cur.fetchall()

    return rows


def main(receiverCol, senderCol):
    database = r"C:\Users\johnh\Desktop\SJSU-Archer-FlaskChat_v7WORKING\app\db.sqlite3"

    # Create database connection
    conn = create_connection(database)

    chatLog = select_task_by_priority(conn, receiverCol, senderCol)
    with conn:

        print("ReceiverCol: ", receiverCol, " | SenderCol: ", senderCol)

        for chat in chatLog:
            print(chat)

        return chatLog


### ----CHAT CODE  END---------------------------------------------------------------------------------------


### ----FREIND CODE ---------------------------------------------------------------------------------------
@app.route('/add_friend/<username>')
@login_required
def addFriend(username):
    user = User.query.filter_by(username=username).first()
    current_user.befriend(user)
    db.session.commit()
    flash('Friend Added!')
    if user.isFriendsWith(current_user):
        return redirect(url_for('user', user))
    return redirect(url_for('userProfile', username=username))


@app.route('/profile/majorMatch')
@login_required
def majorMatch():
    # finds relation of current user
    match = Survey.query.filter_by(user_id=current_user.id).first()
    # gets major of current user
    # finds data of all other users with same major
    foundMatch = Survey.query.filter_by(major=match.major).all()
    # find corresponding link between user_id and user

    return render_template('majorMatch_Bootstrap.html', title="Your Matches by Major", foundMatch=foundMatch)


@app.route('/profile/indoorMatch')
@login_required
def indoorMatch():
    # finds relation of current user
    match = Survey.query.filter_by(user_id=current_user.id).first()
    # gets indoor interests of current user
    match.indoor
    # finds data of all other users with same indoor interests
    foundMatch = Survey.query.filter_by(indoor=match.indoor)

    return render_template('indoorMatch_Bootstrap.html', title="Your Matches by Interests", foundMatch=foundMatch)


@app.route('/profile/outdoorMatch')
@login_required
def outdoorMatch():
    # finds relation of current user
    match = Survey.query.filter_by(user_id=current_user.id).first()
    # gets outdoor interests of current user
    match.outdoor
    # finds data of all other users with same outdoor interests
    foundMatch = Survey.query.filter_by(outdoor=match.outdoor)

    return render_template('outdoorMatch_Bootstrap.html', title="Your Matches by Interests", foundMatch=foundMatch)


### ----FREIND CODE  END---------------------------------------------------------------------------------------


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('homePage'))
