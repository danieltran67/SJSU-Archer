import os
baseDirectory = os.path.abspath(os.path.dirname(__file__))
#locate database to be in same working __file__
class Config(obj):
    secret_key = os.environ.get("secret_key") or "its a secrete"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
    'sqlite:///' + os.path.join(baseDirectory, 'archer.db') #locates database

    SQLALCHEMY_TRACK_MODS= False #logs any changes
