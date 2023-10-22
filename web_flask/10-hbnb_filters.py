#!/usr/bin/python3
""" script that starts a Flask web application. """

from flask import Flask, render_template
from models import *
from models.state import State
app = Flask(__name__)


def hbnb_filter():
    """ HTML page like 6-index.html from the static project"""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception=None):
    """ Remove SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
