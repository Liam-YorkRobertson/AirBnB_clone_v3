#!/usr/bin/python3
"""
Index for v1 views
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route(("/status"), methods=["GET"], strict_slashes=False)
def status():
    """
    Returns the status
    """
    return (jsonify({"status": "OK"}))
