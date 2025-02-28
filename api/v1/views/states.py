#!/usr/bin/python3
"""
New view for state objects that handles all default restful api actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """
    Retrieves list of all state objects
    """
    states = storage.all(State).values()
    state_dictionaries = [
        state.to_dict()
        for state in states
    ]
    return (jsonify(state_dictionaries))


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_single_state(state_id):
    """
    Retrieves a state object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_state(state_id):
    """
    Deletes a state object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_new_state():
    """
    Creates a state object
    """
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return (jsonify({"error": "Missing name"}), 400)
    new_state = State()
    for key, value in data.items():
        setattr(new_state, key, value)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_existing_state(state_id):
    """
    Updates a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return (jsonify(state.to_dict()), 200)
