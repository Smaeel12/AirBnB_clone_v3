#!/usr/bin/python3
"""
Blueprint for handling all default RestFul API actions for cities
"""
from flask import Blueprint, jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City
from flasgger.utils import swag_from

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
def get_cities(state_id):
    """Retrieves the list of all cities objects of a specific State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<string:city_id>/',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get_city.yml', methods=['GET'])
def get_city(city_id):
    """Retrieves a specific city based on ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city based on ID provided"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city/post_city.yml', methods=['POST'])
def post_city(state_id):
    """Creates a new City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in req_data:
        return jsonify({'error': 'Missing name'}), 400

    new_city = City(state_id=state_id, **req_data)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'], strict_slashes=False)
@swag_from('documentation/city/put_city.yml', methods=['PUT'])
def put_city(city_id):
    """Updates a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req_data = request.get_json()
    if not req_data:
        return jsonify({'error': 'Not a JSON'}), 400

    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in req_data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
