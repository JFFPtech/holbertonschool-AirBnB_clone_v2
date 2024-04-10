#!/usr/bin/python3
"""Module to start a Flask web application with database connection."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database connection configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.getenv("HBNB_MYSQL_USER")}:{os.getenv("HBNB_MYSQL_PWD")}@{os.getenv("HBNB_MYSQL_HOST")}/{os.getenv("HBNB_MYSQL_DB")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.String(60), primary_key=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)

@app.route('/states_list', strict_slashes=False)
def states_list():
    states = State.query.order_by(State.name).all()
    return render_template('7-states_list.html', states=states)

@app.teardown_appcontext
def teardown_db(exception):
    db.session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
