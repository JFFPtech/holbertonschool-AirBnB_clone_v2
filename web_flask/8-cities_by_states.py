#!/usr/bin/python3
"""Module to start a Flask web application with database connection."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import State, City

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
    """
    Represents a city in the database.

    Attributes:
        id (int): The unique identifier for the city.
        name (str): The name of the city.
        state_id (int): The foreign key referencing the associated state.
    """
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    states = State.query.all()
    return render_template('8-cities_by_states.html', states=states)

@app.teardown_appcontext
def teardown_db(exception):
    db.session.remove()

if __name__ == '__main__':
    with app.app_context():
        # It's a good practice to create tables automatically if they don't exist yet.
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
