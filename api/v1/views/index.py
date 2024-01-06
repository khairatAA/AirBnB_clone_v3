#!/usr/bin/pyhton3
"""index module"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    """get_status: gets the status of the API"""
    status_check = {"status": "OK"}
    return jsonify(status_check)
