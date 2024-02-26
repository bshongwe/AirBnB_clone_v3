#!/usr/bin/python3
"""
states
"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
import json
from models import storage
from models.state import State


"""app = Flask(__name__)"""


@app_views.route('/states', strict_slashes=False)
def ret_states():
    """retreives one state"""
    states = storage.all(State)
    j = []
    for obj in states.values():
        j.append(obj.to_dict())
    return (jsonify(j))


@app_views.route('/states/<state_id>', strict_slashes=False)
def ret_state_id(state_id):
    """retreives a state"""
    states = storage.all(State)
    j = []
    for obj in states.values():
        if obj.to_dict()["id"] == state_id:
            j.append(obj.to_dict())
    if len(j) == 0:
        abort(404)
    return (jsonify(j[0]))


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_state_id(state_id):
    """deletes a state"""
    obj = storage.get(State, state_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return (make_response(jsonify({}), 200))

    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def ctreate_state():
    """creates a state"""
    http_data = request.get_json()
    if not http_data:
        abort(400, "Not a JSON")
    if not http_data['name']:
        abort(400, "Missing name")
    new_obj = State(**http_data)
    storage.new(new_obj)
    storage.save()
    return (make_response((new_obj.to_dict()), 201))


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates a state"""
    http_data = request.get_json()
    if not http_data:
        abort(400, "Not a JSON")

    obj = storage.get(State, state_id)
    if obj is not None:
        for key, value in http_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj, key, value)
        storage.save()
        return (make_response((obj.to_dict()), 200))

    else:
        abort(404)
