#!/usr/bin/python3
"""
New view for review objects that handles all default retsful api actions.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """
    Retrieves list of all review objects of a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    review_dictionaries = [
        review.to_dict()
        for review in reviews
    ]
    return (jsonify(review_dictionaries))


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_single_review(review_id):
    """
    Retrieves a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return (jsonify(review.to_dict()))


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_review(review_id):
    """
    Deletes a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return ({}, 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_new_review(place_id):
    """
    Creates a review object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in data:
        return (jsonify({"error": "Missing user_id"}), 400)
    if "text" not in data:
        return (jsonify({"error": "Missing text"}), 400)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    new_review = Review()
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(new_review, key, value)
    new_review.place_id = place_id
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_existing_review(review_id):
    """
    Updates a review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return (jsonify(review.to_dict()), 200)
