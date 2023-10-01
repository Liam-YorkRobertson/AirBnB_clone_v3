#!/usr/bin/python3
"""
Main module for the API for the AirBnB clone.
"""
from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Closes storage
    """
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
