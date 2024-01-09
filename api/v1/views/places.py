#!/usr/bin/python3
"""View for Places objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
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


@app_views.route(
        '/places/<string:id>',
        methods=['GET'],
        strict_slashes=False
        )
def get_place(id):
    """Retrieves a Place object"""
    for place in storage.all(Place).values():
        if (place.id == id):
            return jsonify(place.to_dict())
    abort(404)


@app_views.route(
        '/places/<string:id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_place(id):
    """Deletes a Place object"""
    for place in storage.all(Place).values():
        if (place.id == id):
            storage.delete(place)
            storage.save()
            return (jsonify({}), 200)
    abort(404)


@app_views.route(
        '/cities/<string:id>/places',
        methods=['POST'],
        strict_slashes=False
        )
def create_place(id):
    """Creates a place object"""
    for city in storage.all(City).values():
        if (city.id == id):
            request_data = request.get_json()

            if request_data:
                if "user_id" not in request_data:
                    return ("Missing user_id", 400)
                if "user_id" in request_data:
                    for user in storage.all(User).values():
                        if (user.id != request_data["user_id"]):
                            abort(404)
                elif "name" not in request_data:
                    return ("Missing name", 400)
                else:
                    place = Place()
                    place.user_id = request_data.get("user_id")
                    place.name = request_data.get("name")
                    place.id = id
                    storage.new(place)
                    storage.save()
                    return (jsonify(place.to_dict()), 201)
            else:
                return ("Not a JSON", 400)

    abort(404)


@app_views.route(
        '/places/<string:id>',
        methods=['PUT'],
        strict_slashes=False
        )
def update_place(id):
    """Updates a Place object"""

    for place in storage.all(Place).values():
        if place.id == id:
            if request.get_json() is None:
                abort(400, description="Not a JSON")

            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

            data = request.get_json()
            for key, value in data.items():
                if key not in ignore:
                    setattr(place, key, value)
            storage.save()

            return (jsonify(place.to_dict()), 200)
    abort(404)
