#!/usr/bin/python3
"""starts a Flask web application"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# register blueprint here
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    """returns an error 404 JSON"""
    return (jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_db(exc=None):
    """closes the storage on end of connection to host"""
    storage.close()


if __name__ == '__main__':

    h_ost = getenv("HBNB_API_HOST", '0.0.0.0')
    p_ort = getenv("HBNB_API_PORT", '5000')
    app.run(host=h_ost, port=p_ort, threaded=True)  # , debug=True)
