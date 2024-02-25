#!/usr/bin/python3
"""
index
"""


from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def ok():
    """status ok"""
    return (jsonify(status="ok"))


@app_views.route('/stats', strict_slashes=False)
def number_objs():
    """returns objects numbers"""
    return (jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        states=storage.count('States'),
        reviews=storage.count('Review'),
        places=storage.count('Place'),
        users=storage.count('User')

        ))
