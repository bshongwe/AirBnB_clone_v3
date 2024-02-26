#!/usr/bin/python3
"""
cities
"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
import json
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


"""app = Flask(__name__)"""


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def ret_reviews(review_id):
    """retreives one city"""
    reviews = storage.get(Review, review_id)
    if not reviews:
        abort(404)
    return (jsonify(reviews.to_dict()))


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def ret_review(place_id):
    """retreives a state"""
    places = storage.get(Place, place_id)
    reviews = []
    if places:
        for review in places.reviews:
            reviews.append(review.to_dict())
        return (jsonify(reviews))
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_review(review_id):
    """deletes a place by id"""
    obj = storage.get(Review, review_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return (make_response(jsonify({}), 200))

    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def ctreate_review(place_id):
    """creates a state"""
    http_data = request.get_json()
    places = storage.get(Place, place_id)
    if not places:
        abort(404)

    if not http_data:
        abort(400, "Not a JSON")

    if 'user_id' not in http_data:
        abort(400, "Missing user_id")
    if 'text' not in http_data:
        abort(400, "Missing text")
    """ get user_id """
    userId = http_data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    new_obj = Review(**http_data)
    setattr(new_obj, 'place_id', place_id)
    storage.new(new_obj)
    storage.save()
    return (make_response((new_obj.to_dict()), 201))


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """updates a city"""
    http_data = request.get_json()
    if not http_data:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if review is not None:
        for key, value in http_data.items():
            if key not in ['id', 'created_at',
                           'place_id', 'user_id', 'updated_at']:
                setattr(review, key, value)
        storage.save()
        return (make_response((review.to_dict()), 200))

    else:
        abort(404)
