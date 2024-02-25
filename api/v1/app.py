#!/user/bin/python3
'''
Creates a Flask app, registers blueprint app_views with the Flask instance 'app'
'''

import os
from flask import flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def call_close(err):
    """storage close()"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
