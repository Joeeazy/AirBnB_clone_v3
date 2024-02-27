#!/usr/bin/python3
"""
Create a new view for the link between Place objects and Amenity objects that
handles all default RESTFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, Place, Amenity

@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'])
def places_amenities(place_id):
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities_list = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities_list)

    if request.method == 'POST':
        amenity_id = request.args.get('amenity_id')
        if amenity_id is None:
            abort(400, description='amenity_id parameter is missing')

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None or amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200
