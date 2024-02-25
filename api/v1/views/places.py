#!/usr/bin/python3
"""view State object handling all default RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place


# returns all Place objects linked to a city_id
@app_views.route(
        '/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def list_place(city_id):
    """retrieves all Place objects of a City"""

    if (storage.get(City, city_id) is None):
        abort(404)
    l_place = []
    for item in storage.all(Place).values():
        if (item.city_id == city_id):
            l_place.append(item.to_dict())

    return (jsonify(l_place))


# retrieves a place object
@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def single_place_retrieval(place_id):
    """retrieves a single city object or raises a 404"""
    rtn_obj = storage.get(Place, place_id)

    if (rtn_obj is None):
        abort(404)
    else:
        return (jsonify(rtn_obj.to_dict()))


# deletes a place object
@app_views.route(
        '/places/<place_id>', strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """deletes a place object """
    del_obj = storage.get(Place, place_id)

    if (del_obj is None):
        abort(404)
    else:
        storage.delete(del_obj)
        storage.save()
        return (jsonify({}))


# creates a place object
@app_views.route(
        '/cities/<city_id>/places', strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """ create a Place Object from a POST request"""

    if (storage.get(City, city_id) is False):
        abort(404)

    creation_obj = request.get_json(silent=True)

    if (isinstance(creation_obj, dict) is False):
        abort(400, "Not a JSON")

    for i in ['user_id', 'name']:
        if (creation_obj.get(i) is None):
            abort(400, f"Missing {i}")

    else:
        creation_obj['city_id'] = city_id
        place_item = Place(**creation_obj)
        place_item.save()
        response = make_response(jsonify(place_item.to_dict()), 201)
        return (response)


# updates a place object
@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ update a Place Object from a PUT request"""

    obj_update = storage.get(Place, place_id)
    creation_obj = None
    if (obj_update is None):
        abort(404)
    else:
        creation_obj = request.get_json(silent=True)

        if (isinstance(creation_obj, dict) is False):
            abort(400, "Not a JSON")

        else:

            ignored = ['id', 'city_id', 'user_id',
                       'created_at', 'updated_at']

            for key, value in creation_obj.items():
                if (key not in ignored):
                    setattr(obj_update, key, value)
            obj_update.save()
            response = make_response(jsonify(obj_update.to_dict()), 200)
            return (response)
