#!/user/bin/python3
'''
This script creates a Flask app and registers blueprint app_views with the Flask instance 'app'
'''

from os import getenv
from flask import flask, jsonify
from flask cors import CORS
from models import storage
from api.v1.views import app_views

app = flask (__name__)

#task 12
#enable CORS and allow request from any origin:
CORS(app, resources={r'api/v1/*': {'origins':'0.0.0.0'}})

#Register the app_views blueprint:
app.register_blueprint(app_views)
app.url_map_srict_slashes = False

#Teardown function to close the SQLA1chemy session object after each request:
@app.teardown_appcontext
def tear down engine (exception):
    '''
    Remove the current SQLA1chemy session oblect after each request.
    '''
    storage.close()

#task 5
#Error handler for 404 Not Found:
@app.errorhandler (404)
def not _found(error):
    '''Return JSON response with "Not Found" error message.
    '''
    response = {'error':'Not Found'}
    return jsonify (response), 404

if __name__ == '__main__':
    #Get the host and port from environment variables.
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    #Run the app in threaded mode for better perfomance:
    app.run (host = HOST, port = PORT, threaded = True
