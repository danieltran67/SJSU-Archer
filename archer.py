from app import app, socketio
from app import manager

"""
if you wish to add another column. add it to User class in models.py
then run the manager.run() below.
then run these commands in the shell
python .\archer.py db init ( do this once)
python .\archer.py db migrate
python .\archer.py db upgrade
"""


#if __name__ =='__main__':
#    manager.run()

socketio.run(app, debug=True)
"""This file runs the website. We separated it so no one touches it."""
#app.run(debug=True)
