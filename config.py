import os
baseDirectory = os.path.abspath(os.path.dirname(__file__))
#locate database to be in same working __file__
class Config(object):
    secret_key = os.environ.get("secret_key") or "its a secret"
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
    'sqlite:///' + os.path.join(baseDirectory, 'archer.db') #locates database

    SQLALCHEMY_TRACK_MODIFICATION= False #logs any changes
