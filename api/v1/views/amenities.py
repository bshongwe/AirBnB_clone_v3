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


"""app = Flask(__name__)"""


@app_views.route('/amenities', strict_slashes=False)
def ret_amenities():
    """retreives one state"""
    amenities = storage.all(Amenity)
    j = []
    for obj in amenities.values():
        j.append(obj.to_dict())
    return (jsonify(j))


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def ret_amenity_c(amenity_id):
    """retreives one amenity"""
    amenties = storage.get(Amenity, amenity_id)
    if not amenties:
        abort(404)
    return (jsonify(amenties.to_dict()))


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def remove_amenity(amenity_id):
    """deletes a amenity"""
    obj = storage.get(Amenity, amenity_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return (make_response(jsonify({}), 200))

    else:
        abort(404)


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def ctreate_amenity():
    """creates a state"""
    http_data = request.get_json()
    if not http_data:
        abort(400, "Not a JSON")
    if not http_data['name']:
        abort(400, "Missing name")

    new_obj = Amenity(**http_data)
    storage.new(new_obj)
    storage.save()
    return (make_response((new_obj.to_dict()), 201))


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updates a city"""
    http_data = request.get_json()
    if not http_data:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        for key, value in http_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return (make_response((amenity.to_dict()), 200))

    else:
        abort(404)
