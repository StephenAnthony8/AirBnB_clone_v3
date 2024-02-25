#!/usr/bin/python3
"""view State object handling all default RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


# returns all City objects linked to a state_id
@app_views.route(
        '/states/<state_id>/cities', strict_slashes=False, methods=['GET'])
def list_city(state_id):
    """retrieves all City objects of a State"""

    if (storage.get(State, state_id) is None):
        abort(404)
    l_city = []
    for item in storage.all(City).values():
        if (item.state_id == state_id):
            l_city.append(item.to_dict())

    return jsonify(l_city)


# retrieves a city object
@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def single_city_retrieval(city_id):
    """retrieves a single city object or raises a 404"""
    rtn_obj = storage.get(City, city_id)

    if (rtn_obj is None):
        abort(404)
    else:
        return (jsonify(rtn_obj.to_dict()))


# deletes a city object
@app_views.route(
        '/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """deletes a city object """
    del_obj = storage.get(City, city_id)

    if (del_obj is None):
        abort(404)
    else:
        storage.delete(del_obj)
        storage.save()
        return (jsonify({}))


# creates a city object
@app_views.route(
        '/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """ create a City Object from a POST request"""

    if (storage.get(State, state_id) is False):
        abort(404)

    creation_obj = request.get_json(silent=True)

    if (isinstance(creation_obj, dict) is False):
        abort(400, "Not a JSON")

    elif (creation_obj.get('name') is None):
        abort(400, "Missing name")

    else:
        creation_obj['state_id'] = state_id
        city_item = City(**creation_obj)
        city_item.save()
        response = make_response(jsonify(city_item.to_dict()), 201)
        return (response)


# updates a city object
@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ update a City Object from a PUT request"""

    obj_update = storage.get(City, city_id)
    creation_obj = None
    if (obj_update is None):
        abort(404)
    else:
        creation_obj = request.get_json(silent=True)

        if (isinstance(creation_obj, dict) is False):
            abort(400, "Not a JSON")

        else:

            ignored = ['id', 'created_at', 'updated_at', 'state_id']
            for key, value in creation_obj.items():
                if (key not in ignored):
                    setattr(obj_update, key, value)
            obj_update.save()
            response = make_response(jsonify(obj_update.to_dict()), 200)
            return (response)
