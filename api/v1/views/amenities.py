#!/usr/bin/python3
"""
New view for amenity objects that handles all default restful api actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """
    Retrieves list of all amenity objects
    """
    amenities = storage.all(Amenity).values()
    amenity_dictionaries = [
        amenity.to_dict()
        for amenity in amenities
    ]
    return (jsonify(amenity_dictionaries))


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_single_amenity(amenity_id):
    """
    Retrieves an amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return (jsonify(amenity.to_dict()))


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_amenity(amenity_id):
    """
    Deletes an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_new_amenity():
    """
    Creates an Amenity object
    """
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return (jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity()
    for key, value in data.items():
        setattr(new_amenity, key, value)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_existing_amenity(amenity_id):
    """
    Updates an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
