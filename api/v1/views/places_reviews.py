#!/usr/bin/python3
"""Review API endpoints."""
from flask import jsonify, request, abort, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def place_reviews(place_id):
    """Handles GET and POST requests for reviews of a place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify([review.to_dict() for review in place.reviews])

    elif request.method == 'POST':
        data = request.get_json()
        if not data or type(data) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        user_id = data.get('user_id')
        if not storage.get('User', user_id):
            abort(404)
        if 'text' not in data:
            return jsonify({'error': 'Missing text'}), 400

        new_review = Review(place_id=place_id, **data)
        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def review(review_id):
    """Handles GET, PUT, and DELETE requests for a review."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        if not data or type(data) is not dict:
            return jsonify({'error': 'Not a JSON'}), 400

        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
