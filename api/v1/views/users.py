#!/usr/bin/python3
"""
New view for user objects that handles all default restful api actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    Retrieves list of all User objects
    """
    users = storage.all(User).values()
    user_dictionaries = [
        user.to_dict()
        for user in users
    ]
    return (jsonify(user_dictionaries))


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_single_user(user_id):
    """
    Retrieves a user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return (jsonify(user.to_dict()))


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_user(user_id):
    """
    Deletes a user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_new_user():
    """
    Creates a user object
    """
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "email" not in data:
        return (jsonify({"error": "Missing email"}), 400)
    if "password" not in data:
        return (jsonify({"error": "Missing password"}), 400)
    new_user = User()
    for key, value in data.items():
        setattr(new_user, key, value)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_existing_user(user_id):
    """
    Updates a user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return (jsonify(user.to_dict()), 200)
