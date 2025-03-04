#!/usr/bin/python3
""" script that starts a Flask web application. """

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ HTML page with list of states sorted by name """
    states = sorted(storage.all(State).values(), key=lambda i: i.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception=None):
    """ Remove SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
