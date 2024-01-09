#!/usr/bin/python3
"""view for Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities_list():
    """Retrieves the list of all amenities objects"""
    amenities = storage.all(Amenity).values()

    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route(
        '/amenities/<string:id>',
        methods=['GET'],
        strict_slashes=False
        )
def get_amenity(id):
    """Retrieves an Amenity object"""
    for amenity in storage.all(Amenity).values():
        if (amenity.id == id):
            return jsonify(amenity.to_dict())

    abort(404)


@app_views.route(
        '/amenities/<string:id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_amenity(id):
    """Deletes an Amenity object"""
    for amenity in storage.all(Amenity).values():
        if (amenity.id == id):
            storage.delete(amenity)
            storage.save()
            return jsonify({}, 200)

    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity"""
    request_data = request.get_json()

    if request_data:
        if "name" not in request_data:
            return ("Missing name", 400)
        else:
            amenity = Amenity()
            amenity.name = request_data.get("name")
            storage.new(amenity)
            storage.save()
            return jsonify(amenity.to_dict(), 201)
    else:
        return ("Not a JSON", 400)


@app_views.route(
        '/amenities/<string:id>',
        methods=['PUT'],
        strict_slashes=False
        )
def update_amenity(id):
    """
    Updates an Amenity
    """
    for amenity in storage.all(Amenity).values():
        if amenity.id == id:
            if request.get_json() is None:
                abort(400, description="Not a JSON")

            ignore = ['id', 'created_at', 'updated_at']

            data = request.get_json()
            for key, value in data.items():
                if key not in ignore:
                    setattr(amenity, key, value)

            storage.save()

            return (jsonify(amenity.to_dict()), 200)

    abort(404)
