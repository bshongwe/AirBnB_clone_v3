#!/usr/bin/python3
"""
amenities
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
import json
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


"""app = Flask(__name__)"""


@app_views.route('/users', strict_slashes=False)
def ret_users():
    """retreives one state"""
    users = storage.all(User)
    j = []
    for obj in users.values():
        j.append(obj.to_dict())
    return (jsonify(j))


@app_views.route('/users/<user_id>', strict_slashes=False)
def ret_user(user_id):
    """retreives one amenity"""
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    return (jsonify(users.to_dict()))


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_user(user_id):
    """deletes a amenity"""
    obj = storage.get(User, user_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return (make_response(jsonify({}), 200))

    else:
        abort(404)


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def ctreate_user():
    """creates a state"""
    http_data = request.get_json()
    if not http_data:
        abort(400, "Not a JSON")
    if not http_data['email']:
        abort(400, "Missing email")
    if not http_data['password']:
        abort(400, "Missing password")

    new_obj = User(**http_data)
    storage.new(new_obj)
    storage.save()
    return (make_response((new_obj.to_dict()), 201))


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates a city"""
    http_data = request.get_json()
    if not http_data:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if user is not None:
        for key, value in http_data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        storage.save()
        return (make_response((user.to_dict()), 200))

    else:
        abort(404)
