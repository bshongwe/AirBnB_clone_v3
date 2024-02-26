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


"""app = Flask(__name__)"""


@app_views.route('/places/<place_id>', strict_slashes=False)
def ret_place(place_id):
    """retreives one city"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    return (jsonify(places.to_dict()))


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def ret_city_id_c(city_id):
    """retreives a state"""
    cities = storage.get(City, city_id)
    places = []
    if cities:
        for place in cities.places:
            places.append(place.to_dict())
        return (jsonify(places))
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_place(place_id):
    """deletes a place by id"""
    obj = storage.get(Place, place_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return (make_response(jsonify({}), 200))

    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def ctreate_place(city_id):
    """creates a state"""
    http_data = request.get_json()
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)

    if not http_data:
        abort(400, "Not a JSON")
    if 'name' not in http_data:
        abort(400, "Missing name")
    if 'user_id' not in http_data:
        abort(400, "Missing user_id")
    """ get user_id """
    userId = http_data['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    new_obj = Place(**http_data)
    setattr(new_obj, 'city_id', city_id)
    storage.new(new_obj)
    storage.save()
    return (make_response((new_obj.to_dict()), 201))


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a city"""
    http_data = request.get_json()
    if not http_data:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is not None:
        for key, value in http_data.items():
            if key not in ['id', 'created_at',
                           'city_id', 'user_id', 'updated_at']:
                setattr(place, key, value)
        storage.save()
        return (make_response((place.to_dict()), 200))

    else:
        abort(404)
