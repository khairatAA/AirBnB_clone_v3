#!/usr/bin/python3
"""view for User objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.base_model import BaseModel


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users_list():
    """get_users_list: Retrieves the list of all Users objects"""
    users = storage.all(User).values()

    users_list = []
    for user in users:
        users_list.append(user.to_dict())

    return jsonify(users_list)


@app_views.route('/users/<string:id>', methods=['GET'], strict_slashes=False)
def get_user(id):
    """Retrieves a User object"""
    for user in storage.all(User).values():
        if (user.id == id):
            return jsonify(user.to_dict())

    abort(404)


@app_views.route(
        '/users/<string:id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_user(id):
    """Deletes a User object"""
    for user in storage.all(User).values():
        if (user.id == id):
            storage.delete(user)
            storage.save()
            return jsonify({}, 200)

    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    request_data = request.get_json()

    if request_data:
        if "name" not in request_data:
            return ("Missing name", 400)
        else:
            user = User()
            user.name = request_data.get("name")
            storage.new(user)
            storage.save()
            return jsonify(user.to_dict(), 201)
    else:
        return ("Not a JSON", 400)


@app_views.route('/users/<string:id>', methods=['PUT'], strict_slashes=False)
def update_users(id):
    """
    Updates User
    """
    for user in storage.all(User).values():
        if user.id == id:
            if request.get_json() is None:
                abort(400, description="Not a JSON")

            ignore = ['id', 'created_at', 'updated_at']

            data = request.get_json()
            for key, value in data.items():
                if key not in ignore:
                    setattr(user, key, value)

            storage.save()

            return (jsonify(user.to_dict()), 200)

    abort(404)
