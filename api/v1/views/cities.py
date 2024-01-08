#!/usr/bin/python3
"""
View for Cities in a State objects that
handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from models.base_model import BaseModel


@app_views.route(
        '/states/<string:state_id>/cities',
        methods=['GET'],
        strict_slashes=False
        )
def get_cities_from_state(state_id):
    """Retrieves the list of all City objects of a State"""
    cities_list = []

    for state in storage.all(State).values():
        if (state.id == state_id):
            for city in state.cities:
                cities_list.append(city.to_dict())
            return jsonify(cities_list)

    abort(404)


@app_views.route(
        '/cities/<string:city_id>',
        methods=['GET'],
        strict_slashes=False
        )
def get_city(city_id):
    """Retrieves a City object"""
    for city in storage.all(City).values():
        if (city.id == city_id):
            return jsonify(city.to_dict())
    abort(404)


@app_views.route(
        '/cities/<string:city_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_city(city_id):
    """Deletes a City object"""
    for city in storage.all(City).values():
        if (city.id == city_id):
            storage.delete(city)
            storage.save()
            return (jsonify({}), 200)
    abort(404)


@app_views.route(
        '/states/<string:state_id>/cities',
        methods=['POST'],
        strict_slashes=False
        )
def create_city(state_id):
    """Creates a city object"""
    for state in storage.all(State).values():
        if (state.id == state_id):
            request_data = request.get_json()

            if request_data:
                if "name" not in request_data:
                    return ("Missing name", 400)
                else:
                    city = City()
                    city.name = request_data.get("name")
                    city.state_id = state_id
                    storage.new(city)
                    storage.save()
                    return (jsonify(city.to_dict()), 201)
            else:
                return ("Not a JSON", 400)

    abort(404)


@app_views.route(
        '/cities/<string:city_id>',
        methods=['PUT'],
        strict_slashes=False
        )
def update_city(city_id):
    """Updates a City object"""
    print(f'City: {city_id}')

    for city in storage.all(City).values():
        if city.id == city_id:
            print(f'City info: {city}')
            if request.get_json() is None:
                abort(400, description="Not a JSON")

            ignore = ['id', 'state_id', 'created_at', 'updated_at']

            data = request.get_json()
            for key, value in data.items():
                if key not in ignore:
                    setattr(city, key, value)

            storage.save()
            print(f'Updated info: {city}')

            return (jsonify(city.to_dict()), 200)
    abort(404)
