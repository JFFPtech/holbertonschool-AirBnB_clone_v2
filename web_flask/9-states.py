#!/usr/bin/python3
"""Module to start a Flask web application with database connection."""
from flask import Flask, render_template
from models.engine.db_storage import DBStorage
from models.state import State

app = Flask(__name__)

storage = DBStorage()
storage.reload()

@app.route('/states', strict_slashes=False)
def states():
    all_states = storage.all(State)
    sorted_states = sorted(all_states.values(), key=lambda state: state.name)
    return render_template('9-states.html', states=sorted_states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Displays an HTML page with info about <id>, if it exists."""
    state = storage.get(State, id)
    if state is None:
        return "State not found", 404
    return render_template("9-states.html", state=state)

@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the database connection."""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)