#!/user/bin/python3
'''
Creates a Flask app, registers blueprint app_views with the Flask instance 'app'
'''

import os
from flask import flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = flask (__name__)

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
    return make_response(jsonify(response), 404)

if __name__ == '__main__':
    #Get the host and port from environment variables.
    HOST = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    PORT = int(os.environ.get('HBNB_API_PORT', 5000))
    #Run the app in threaded mode for better perfomance:
    app.run (host = HOST, port = PORT, threaded = True)
