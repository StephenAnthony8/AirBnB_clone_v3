#!/usr/bin/python3
"""view State object handling all default RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


# returns all amenity objects linked to a state_id
@app_views.route(
        '/amenities', strict_slashes=False, methods=['GET'])
def list_amenity():
    """retrieves all Amenity objects"""

    l_amenity = []
    for item in storage.all(Amenity).values():
        l_amenity.append(item.to_dict())

    return jsonify(l_amenity)


# retrieves an amenity object
@app_views.route(
        '/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def single_amenity_retrieval(amenity_id):
    """retrieves a single amenity object or raises a 404"""
    rtn_obj = storage.get(Amenity, amenity_id)

    if (rtn_obj is None):
        abort(404)
    else:
        return (jsonify(rtn_obj.to_dict()))


# deletes an amenity object
@app_views.route(
        '/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """deletes an amenity object """
    del_obj = storage.get(Amenity, amenity_id)

    if (del_obj is None):
        abort(404)
    else:
        storage.delete(del_obj)
        storage.save()
        return (jsonify({}))


# creates an amenity object
@app_views.route(
        '/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """ create an Amenity Object from a POST request"""

    creation_obj = request.get_json(silent=True)

    if (isinstance(creation_obj, dict) is False):
        abort(400, "Not a JSON")

    elif (creation_obj.get('name') is None):
        abort(400, "Missing name")

    else:
        amenity_item = Amenity(**creation_obj)
        amenity_item.save()
        response = make_response(jsonify(amenity_item.to_dict()), 201)
        return (response)


# updates an Amenity object
@app_views.route(
        '/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """ update an Amenity Object from a PUT request"""

    obj_update = storage.get(Amenity, amenity_id)
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
