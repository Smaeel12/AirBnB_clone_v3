#!/usr/bin/python3
"""
Blueprint for handling all default RestFul API actions for Amenity objects
"""


from flask import Blueprint, jsonify, request, abort, make_response
from flasgger.utils import swag_from
from models import storage
from models.amenity import Amenity

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml')
def get_amenities():
    """Retrieves a list of all amenities"""
    all_amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in all_amenities])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a specific amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a specific amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def post_amenity():
    """Creates a new amenity"""
    post_data = request.get_json()
    if not post_data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in post_data:
        return jsonify({'error': 'Missing name'}), 400
    new_amenity = Amenity(**post_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def put_amenity(amenity_id):
    """Updates a specific amenity by ID"""
    put_data = request.get_json()
    if not put_data:
        return jsonify({'error': 'Not a JSON'}), 400

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    for key, value in put_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
