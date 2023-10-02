#!/usr/bin/python3
"""
New view for the relationship between Place and Amenity objects
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves list of all amenity objects of a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    amenity_dictionaries = [amenity.to_dict() for amenity in amenities]
    return (jsonify(amenity_dictionaries))


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes an amenity object from a place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Links an amenity object to a place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return (jsonify(amenity.to_dict()), 200)
    place.amenities.append(amenity)
    storage.save()
    return (jsonify(amenity.to_dict()), 201)
