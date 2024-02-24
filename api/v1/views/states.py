#!/usr/bin/python3
"""view State object handling all default RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
import json


# returns all State objects
@app_views.route('/states', strict_slashes=False, methods=['GET'])
def list_state():
    """retrieves all State objects"""
    l_state = []
    for item in storage.all(State).values():
        l_state.append(item.to_dict())

    return jsonify(l_state)


# retrieves a state object
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def single_state_retrieval(state_id):
    """retrieves a single state object or raises a 404"""
    rtn_obj = storage.get(State, state_id)

    if (rtn_obj is None):
        abort(404)
    else:
        return (jsonify(rtn_obj.to_dict()))


# deletes a state object
@app_views.route(
        '/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """deletes a state object """
    del_obj = storage.get(State, state_id)

    if (del_obj is None):
        abort(404)
    else:
        storage.delete(del_obj)
        storage.save()
        return (jsonify({}))


# creates a state object
@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """ create a State Object from a POST request"""

    creation_obj = request.get_json(silent=True)

    if (isinstance(creation_obj, dict) is False):
        abort(400, "Not a JSON")

    elif (creation_obj.get('name') is None):
        abort(400, "Missing name")

    else:
        state_item = State(**creation_obj)
        state_item.save()
        response = make_response(jsonify(state_item.to_dict()), 201)
        return (response)


# updates a state object
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ update a State Object from a PUT request"""

    obj_update = storage.get(State, state_id)
    creation_obj = None
    if (obj_update is None):
        abort(404)
    else:
        creation_obj = request.get_json(silent=True)

        if (isinstance(creation_obj, dict) is False):
            abort(400, "Not a JSON")

        else:

            ignored = ['id', 'created_at', 'updated_at']
            for key, value in creation_obj.items():
                if (key not in ignored):
                    setattr(obj_update, key, value)
            obj_update.save()
            response = make_response(jsonify(obj_update.to_dict()), 200)
            return (response)
