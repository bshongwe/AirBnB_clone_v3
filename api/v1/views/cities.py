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


"""app = Flask(__name__)"""


@app_views.route('/cities/<city_id>', strict_slashes=False)
def ret_city_c(city_id):
    """retreives one city"""
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    return (jsonify(cities.to_dict()))


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def ret_state_id_c(state_id):
    """retreives a state"""
    states = storage.get(State, state_id)
    cities = []
    if states:
        for city in states.cities:
            cities.append(city.to_dict())
        return (jsonify(cities))
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_city(city_id):
    """deletes a city"""
    obj = storage.get(City, city_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return (make_response(jsonify({}), 200))

    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def ctreate_city(state_id):
    """creates a state"""
    http_data = request.get_json()
    state = storage.get(State, state_id)
    if not http_data:
        abort(400, "Not a JSON")
    if not http_data['name']:
        abort(400, "Missing name")

    new_obj = City(**http_data)
    setattr(new_obj, 'state_id', state_id)
    storage.new(new_obj)
    storage.save()
    return (make_response((new_obj.to_dict()), 201))


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """updates a city"""
    http_data = request.get_json()
    if not http_data:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is not None:
        for key, value in http_data.items():
            if key not in ['id', 'created_at', 'state_id', 'updated_at']:
                setattr(city, key, value)
        storage.save()
        return (make_response((city.to_dict()), 200))

    else:
        abort(404)
