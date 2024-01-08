#!/usr/bin/python3
"""
View for User objects that handles all default RESTFul API actions
"""
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
            return (jsonify({}), 200)

    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates User"""
    request_data = request.get_json()

    if request_data:
        if "email" not in request_data:
            return ("Missing email", 400)
        elif "password" not in request_data:
            return ("Missing password", 400)
        else:
            user = User()
            user.email = request_data.get("email")
            user.password = request_data.get("password")
            storage.new(user)
            storage.save()
            return (jsonify(user.to_dict()), 201)
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

            ignore = ['id', 'email', 'created_at', 'updated_at']

            data = request.get_json()
            for key, value in data.items():
                if key not in ignore:
                    setattr(user, key, value)

            storage.save()

            return (jsonify(user.to_dict()), 200)

    abort(404)
