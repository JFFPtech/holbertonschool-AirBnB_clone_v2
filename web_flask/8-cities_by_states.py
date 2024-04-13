#!/usr/bin/python3
"""Module to start a Flask web application with database connection."""
from os import getenv
from flask import Flask, render_template
from models import State, City
from models import storage
from sqlalchemy.inspection import inspect

app = Flask(__name__)

storage.reload()


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Shutdown the current session."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def states_list():
    """Display all states with the id and sorted by the name."""
    new_dict = dict(sorted(storage.all(State).items(),
                    key=lambda item: item[1].name))
    return render_template('8-cities_by_states.html', states=new_dict.values())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
