#!/usr/bin/python3
"""
index
"""


from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def api_status():
    """status ok"""
    response = {'status': 'OK'}
    return jsonify(response)

#task 4
@app_views.route('/status', methods=['GET'])
def get_status():
    """retrieve number of each objects by type"""
    status = {
    'amenities': storage.count('Amenity'),
    'cities': storage.count('City'),
    'states': storage.count('States'),
    'reviews': storage.count('Review'),
    'places': storage.count('Place'),
    'users': storage.count('User')
        
        }
    return jsonify(status)
