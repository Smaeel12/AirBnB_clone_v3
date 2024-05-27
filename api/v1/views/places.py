#!/usr/bin/python3
"""
Blueprint for handling all default RestFul API actions for places
"""
from flask import Blueprint, jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.city import City

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """Handles all default RestFul API actions for places."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    elif request.method == 'POST':
        data = request.get_json()
        if not data or type(data) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        user_id = data.get('user_id')
        if not storage.get('User', user_id):
            abort(404)
        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400

        new_place = Place(city_id=city_id, **data)
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place(place_id):
    """Handles specific place by ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not data or type(data) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400

        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
