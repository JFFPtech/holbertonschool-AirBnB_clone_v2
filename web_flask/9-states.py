#!/usr/bin/python3
"""Module to start a Flask web application with database connection."""
from flask import Flask, render_template
from models.state import State, City
from os import getenv
from models import storage
from sqlalchemy.inspection import inspect

app = Flask(__name__)


storage.reload()


@app.route('/states', strict_slashes=False)
def state_list():
    """Display all states with the id and sorted by the name."""
    new_dict = dict(sorted(storage.all(State).items(),
                    key=lambda item: item[1].name))
    return render_template('8-cities_by_states.html', states=new_dict.values())


@app.route("/states/<id>", strict_slashes=False)
def state_list_id(id):
    """Displays an HTML page with info about <id>, if it exists."""
    new_dict = dict(sorted(storage.all(State).items(),
                    key=lambda item: item[1].name))
    for state in new_dict.values():
        if state.id == id:
            return render_template('9-states.html', state=state)
    return "Not found!", 404


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the database connection."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
