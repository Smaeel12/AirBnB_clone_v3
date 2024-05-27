#!/usr/bin/python3
"""
Module for handling all default RestFul API actions for Users
"""
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models import storage
from models.user import User
from api.v1.views import app_views


# Helper function to retrieve a user by ID or abort with 404
def get_user_or_abort(user_id):
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    return user


# Helper function to parse JSON from request or abort with 400
def parse_json_or_abort():
    data = request.get_json()
    if not data or not isinstance(data, dict):
        abort(400, description="Invalid JSON")
    return data


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    if request.method == 'GET':
        return jsonify([user.to_dict() for user
                       in storage.all('User').values()])
    elif request.method == 'POST':
        data = parse_json_or_abort()
        if 'email' not in data or 'password' not in data:
            abort(400, description="Missing required fields")
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_user_id(user_id):
    user = get_user_or_abort(user_id)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        data = parse_json_or_abort()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
