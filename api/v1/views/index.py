#!/usr/bin/python3
"""index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review


@app_views.route('/status')
def get_status():
    """get_status: gets the status of the API"""
    status_check = {"status": "OK"}
    return jsonify(status_check)

@app_views.route('/stats')
def retrieve_object_number():
    """Retrieves the number of each objects by type"""
    object_list = [Amenity, City, Place, Review, State, User]
    name_list = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']

    object_dict ={}
    for index, object in enumerate(object_list):
        object_count = storage.count(object)
        object_dict[name_list[index]] = object_count

    return jsonify(object_dict)
