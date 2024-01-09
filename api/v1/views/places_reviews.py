#!/usr/bin/python3
"""View for Places objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from models.base_model import BaseModel


@app_views.route(
        '/places/<string:place_id>/reviews',
        methods=['GET'],
        strict_slashes=False
        )
def get_review_from_place(place_id):
    """Retrieves the list of all Reviews objects of a Place"""
    review_list = []

    for place in storage.all(Place).values():
        if (place.id == place_id):
            for review in place.id:
                review_list.append(review.to_dict())
            return jsonify(review_list)

    abort(404)


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['GET'],
        strict_slashes=False
        )
def get_review(review_id):
    """Retrieves a Review object"""
    for review in storage.all(Review).values():
        if (review.id == review_id):
            return jsonify(review.to_dict())
    abort(404)


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_review(review_id):
    """Deletes a review object"""
    for review in storage.all(Review).values():
        if (review.id == review_id):
            storage.delete(review)
            storage.save()
            return (jsonify({}), 200)
    abort(404)


@app_views.route(
        '/places/<string:place_id>/reviews',
        methods=['POST'],
        strict_slashes=False
        )
def create_review(place_id):
    """Creates a review object"""
    for place in storage.all(Place).values():
        if (place.id == place_id):
            request_data = request.get_json()

            if request_data:
                if "user_id" not in request_data:
                    return ("Missing user_id", 400)
                elif "user_id" in request_data:
                    for user in storage.all(User).values():
                        if (user.id != request_data["user_id"]):
                            abort(404)
                elif "text" not in request_data:
                    return ("Missing taxt", 400)
                else:
                    review = Review()
                    review.user_id = request_data.get("user_id")
                    review.text = request_data.get("text")
                    place.place_id = place_id
                    storage.new(review)
                    storage.save()
                    return (jsonify(review.to_dict()), 201)
            else:
                return ("Not a JSON", 400)

    abort(404)


@app_views.route(
        '/reviews/<string:review_id>',
        methods=['PUT'],
        strict_slashes=False
        )
def update_review(review_id):
    """Updates a review object"""

    for review in storage.all(Review).values():
        if review.id == review_id:
            if request.get_json() is None:
                abort(400, description="Not a JSON")

            ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

            data = request.get_json()
            for key, value in data.items():
                if key not in ignore:
                    setattr(review, key, value)
            storage.save()

            return (jsonify(review.to_dict()), 200)
    abort(404)
