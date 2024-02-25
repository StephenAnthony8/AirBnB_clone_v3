#!/usr/bin/python3
"""view user object handling all default RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


# returns all user objects
@app_views.route('/users', strict_slashes=False, methods=['GET'])
def list_user():
    """retrieves all user objects"""
    l_user = []
    for item in storage.all(User).values():
        l_user.append(item.to_dict())

    return jsonify(l_user)


# retrieves a user object
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def single_user_retrieval(user_id):
    """retrieves a single user object or raises a 404"""
    rtn_obj = storage.get(User, user_id)

    if (rtn_obj is None):
        abort(404)
    else:
        return (jsonify(rtn_obj.to_dict()))


# deletes a user object
@app_views.route(
        '/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """deletes a user object """
    del_obj = storage.get(User, user_id)

    if (del_obj is None):
        abort(404)
    else:
        storage.delete(del_obj)
        storage.save()
        return (jsonify({}))


# creates a user object
@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """ create a user Object from a POST request"""

    creation_obj = request.get_json(silent=True)

    if (isinstance(creation_obj, dict) is False):
        abort(400, "Not a JSON")

    for i in ['email', 'password']:
        if (creation_obj.get(i) is None):
            abort(400, f"Missing {i}")

    else:
        user_item = User(**creation_obj)
        user_item.save()
        response = make_response(jsonify(user_item.to_dict()), 201)
        return (response)


# updates a user object
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """ update a user Object from a PUT request"""

    obj_update = storage.get(User, user_id)
    creation_obj = None
    if (obj_update is None):
        abort(404)
    else:
        creation_obj = request.get_json(silent=True)

        if (isinstance(creation_obj, dict) is False):
            abort(400, "Not a JSON")

        else:

            ignored = ['id', 'created_at', 'updated_at', 'email']
            for key, value in creation_obj.items():
                if (key not in ignored):
                    setattr(obj_update, key, value)
            obj_update.save()
            response = make_response(jsonify(obj_update.to_dict()), 200)
            return (response)
