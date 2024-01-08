#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states_list():
    """get_states_list: Retrieves the list of all State objects"""
    states = storage.all(State).values()

    states_list = []
    for state in states:
        states_list.append(state.to_dict())

    return jsonify(states_list)


@app_views.route('/states/<string:id>', methods=['GET'], strict_slashes=False)
def get_a_state(id):
    """get_a_state: Retrieves a State object"""
    for state in storage.all(State).values():
        if (state.id == id):
            return jsonify(state.to_dict())

    abort(404)


@app_views.route(
        '/states/<string:id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_a_state(id):
    """Deletes a State object"""
    for state in storage.all(State).values():
        if (state.id == id):
            storage.delete(state)
            storage.save()
            return jsonify({}, 200)

    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    request_data = request.get_json()

    if request_data:
        if "name" not in request_data:
            return ("Missing name", 400)
        else:
            state = State()
            state.name = request_data.get("name")
            storage.new(state)
            storage.save()
            return jsonify(state.to_dict(), 201)
    else:
        return ("Not a JSON", 400)


@app_views.route('/states/<string:id>', methods=['PUT'], strict_slashes=False)
def Update_state(id):
    """
    Updates a State
    """
    for state in storage.all(State).values():
        if state.id == id:
            if request.get_json() is None:
                abort(400, description="Not a JSON")

            ignore = ['id', 'created_at', 'updated_at']

            data = request.get_json()
            for key, value in data.items():
                if key not in ignore:
                    setattr(state, key, value)

            storage.save()

            return (jsonify(state.to_dict()), 200)

    abort(404)
