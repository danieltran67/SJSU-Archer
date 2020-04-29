
import keyring as keyring
import yagmail as yagmail
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

#initialize app, database, and commands

app = Flask(__name__)
SECRET_KEY = 'vnkdjnfjknfl1232#'

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)
Bootstrap(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


yagmail.register('targonthresh@gmail.com', 'a2b2c2d2')
keyring.set_password('yagmail', 'mygmailusername', 'mygmailpassword')
yag = yagmail.SMTP("targonthresh@gmail.com")



#imported after declaring so attributes has chance to be created first
from app import routes, models, form
