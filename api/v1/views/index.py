#!/usr/bin/python3
"""
Blueprint for handling the index and status endpoints for the API
"""
from flask import jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from models.state import State

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Check the status of the API"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def object_status():
    """Retrieves the number of each object by type"""
    objects = {"amenities": 'Amenity', "cities": 'City', "places": 'Place',
               "reviews": 'Review', "states": 'State', "users": 'User'}
    stats = {}
    for key, value in objects.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
