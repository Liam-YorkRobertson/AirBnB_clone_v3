#!/usr/bin/python3
"""
Index for v1 views
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route(("/status"), methods=["GET"], strict_slashes=False)
def status():
    """
    Returns the status
    """
    return (jsonify({"status": "OK"}))


@app_views.route(("/stats"), methods=["GET"], strict_slashes=False)
def stats():
    """
    Returns the number of each object by type
    """
    stats_dictionary = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return (jsonify(stats_dictionary))
