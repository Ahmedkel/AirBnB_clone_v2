#!/usr/bin/python3
""" script that starts a Flask web application. """

from flask import Flask, render_template
from models import *
from models.state import State
app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_list(id=None):
    states = storage.all("State")
    if id:
        key = "State." + id
        state = states.get(key)
    else:
        state = None
    return render_template('9-states.html', states=states, state=state)

@app.teardown_appcontext
def teardown_db(exception=None):
    """ Remove SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
