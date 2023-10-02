#!/usr/bin/python3
"""
Main module for the API for the AirBnB clone.
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Closes storage
    """
    storage.close()


@app.errorhandler(404)
def err(error):
    """
    Handler for 404 errors
    """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return (response)


CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
