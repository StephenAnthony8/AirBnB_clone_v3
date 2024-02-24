#!/usr/bin/python3
"""views blueprint implementation"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def return_status():
    """Returns a STATUS: OK JSON"""
    j_encode = {
        'status': 'OK'
        }

    return (jsonify(j_encode))


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def return_stats():
    """returns a JSON representation of all objects"""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User}
    dict_obj = {}

    for key, value in classes.items():
        dict_obj[key] = storage.count(value)

    return (jsonify(dict_obj))
