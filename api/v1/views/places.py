#!/usr/bin/python3
"""
New view for place objects that handles all default restful api actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_all_places(city_id):
    """
    Retrieves list of all place objects of a city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    place_dictionaries = [
        place.to_dict()
        for place in places
    ]
    return (jsonify(place_dictionaries))


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_single_place(place_id):
    """
    Retrieves a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return (jsonify(place.to_dict()))


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_place(place_id):
    """
    Deletes a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}))


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_new_place(city_id):
    """
    Creates a place object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in data:
        return (jsonify({"error": "Missing user_id"}), 400)
    if "name" not in data:
        return (jsonify({"error": "Missing name"}), 400)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    new_place = Place()
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(new_place, key, value)
    new_place.city_id = city_id
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_existing_place(place_id):
    """
    Updates a place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return (jsonify(place.to_dict()), 200)
