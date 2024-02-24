#!/usr/bin/python3
"""views blueprint implementation"""
# module documentation
from api.v1.views import app_views
from flask import jsonify, request
# create a route '/status' that returns a JSON with status: "ok"


@app_views.route('/status', strict_slashes=False)
def return_status():
    """Returns a 'STATUS: OK' JSON"""
    j_encode = {
        'status': 'OK'
        }

    return (jsonify(j_encode))
