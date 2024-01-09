#!/usr/bin/python3
"""View for Places objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.base_model import BaseModel


@app_views.route(
        'cities/<string:id>/places',
        methods=['GET'],
        strict_slashes=False
        )
def get_place_from_cities(id):
    """Retrieves the list of all Places objects of a City"""
    place_list = []

    for city in storage.all(City).values():
        if (city.id == id):
            for place in city.places:
                place_list.append(place.to_dict())
            return jsonify(place_list)

    abort(404)
