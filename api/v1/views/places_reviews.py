#!/usr/bin/python3
"""view Place object handling all default RESTful API"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review


# returns all Review objects linked to a place_id
@app_views.route(
        '/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def list_review(place_id):
    """retrieves all review objects of a Place"""

    if (storage.get(Place, place_id) is None):
        abort(404)
    l_review = []
    for item in storage.all(Review).values():
        if (item.place_id == place_id):
            l_review.append(item.to_dict())

    return jsonify(l_review)


# retrieves a review object
@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def single_review_retrieval(review_id):
    """retrieves a single review object or raises a 404"""
    rtn_obj = storage.get(Review, review_id)

    if (rtn_obj is None):
        abort(404)
    else:
        return (jsonify(rtn_obj.to_dict()))


# deletes a review object
@app_views.route(
        '/reviews/<review_id>', strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """deletes a review object """
    del_obj = storage.get(Review, review_id)

    if (del_obj is None):
        abort(404)
    else:
        storage.delete(del_obj)
        storage.save()
        return (jsonify({}))


# creates a review object
@app_views.route(
        '/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def create_review(place_id):
    """ create a review Object from a POST request"""

    if (storage.get(Place, place_id) is False):
        abort(404)

    creation_obj = request.get_json(silent=True)

    if (isinstance(creation_obj, dict) is False):
        abort(400, "Not a JSON")

    for i in ['user_id', 'text']:
        if (creation_obj.get(i) is None):
            abort(400, f"Missing {i}")

    else:
        creation_obj['place_id'] = place_id
        review_item = Review(**creation_obj)
        review_item.save()
        response = make_response(jsonify(review_item.to_dict()), 201)
        return (response)


# updates a review object
@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """ update a Review Object from a PUT request"""

    obj_update = storage.get(Review, review_id)
    creation_obj = None
    if (obj_update is None):
        abort(404)
    else:
        creation_obj = request.get_json(silent=True)

        if (isinstance(creation_obj, dict) is False):
            abort(400, "Not a JSON")

        else:

            ignored = ['id', 'place_id', 'user_id',
                       'created_at', 'updated_at']

            for key, value in creation_obj.items():
                if (key not in ignored):
                    setattr(obj_update, key, value)
            obj_update.save()
            response = make_response(jsonify(obj_update.to_dict()), 200)
            return (response)
