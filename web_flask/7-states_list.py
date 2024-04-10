#!/usr/bin/python3
""" Module to start a Flask web application """
from flask import Flask, render_template
import sys
sys.path.append('C:\\Users\\javif\\OneDrive\\Documents\\GitHub\\holbertonschool-AirBnB_clone_v2')
from models import storage

from models import storage

app = Flask(__name__)

@app.route('/states_list', strict_slashes=False)
def states_list():
    states = storage.all("State")
    return render_template('7-states_list.html', states=states)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
