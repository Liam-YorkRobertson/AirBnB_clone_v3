#!/usr/bin/python3
"""
New view for City objects that handles all default RESTful API actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_all_cities(state_id):
    """
    Retrieves list of all city objects of a state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    city_dictionaries = [
        city.to_dict()
        for city in cities
    ]
    return (jsonify(city_dictionaries))


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_single_city(city_id):
    """
    Retrieves a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return (jsonify(city.to_dict()))


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_city(city_id):
    """
    Deletes a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_new_city(state_id):
    """
    Creates a city object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return (jsonify({"error": "Missing name"}), 400)
    new_city = City()
    for key, value in data.items():
        setattr(new_city, key, value)
    new_city.state_id = state_id
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_existing_city(city_id):
    """
    Updates a city object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return (jsonify(city.to_dict()), 200)
