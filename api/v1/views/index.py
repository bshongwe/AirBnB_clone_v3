#!/usr/bin/python3
'''
Create a route '/status' on the object app_views
'''


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    '''
    Return a JSON response for RESFYL API health
    '''
    response = {'status': 'OK'}
    return jsonify(response)

#task 4
@app_views.route('/status', methods=['GET'])
def get_status():
    '''
    retrieve number of each objects by type
    '''
    status = {
    'amenities': storage.count('Amenity'),
    'cities': storage.count('City'),
    'states': storage.count('States'),
    'reviews': storage.count('Review'),
    'places': storage.count('Place'),
    'users': storage.count('User'),
        
        }
    return jsonify(status)
