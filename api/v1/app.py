#!/usr/bin/python3
"""
Create new Flask app, and register blueprint app_views to Flask instance app.
"""

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Task 12
# Enable CORS and allow requests from any origin:
CORS(app, resources={r'/*': {"origins": "0.0.0.0"}})

# Register the app_views blueprint:
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

# Teardown function to close the SQLAlchemy session object after each request:
@app.teardown_appcontext
def teardown_engine(exception):
    """
    Remove the current SQLAlchemy session object after each request.
    """
    storage.close()

# Task 5
# Error handler for 404 Not Found:
@app.errorhandler(404)
def not_found(error):
    """
    Return JSON response with "Not Found" error message.
    """
    response = {'error': 'Not Found'}
    return jsonify(response), 404

if __name__ == '__main__':
    #Get the host and port from environment variables.
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    #Run the app in threaded mode for better perfomance:
    app.run(host=HOST, port=PORT, threaded=True)
