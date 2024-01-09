#!/usr/bin/python3
"""View for Places objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
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
