#!/usr/bin/python3
"""Module to start a Flask web application with database connection."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import State, City
from models import storage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the State model
class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    cities = db.relationship('City', backref='state', lazy=True)

# Define the City model
class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Renders a template that displays a list of states.

    Returns:
        The rendered template with the list of states.
    """
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)

@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    cities = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=cities)

@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
