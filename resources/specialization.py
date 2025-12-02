import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import specializations
from schemas import Specialization_Schema


blp = Blueprint("specializations", __name__, description="Operations on specializations")


@blp.route("/specialization/<string:specialization_id>")
class Specialization(MethodView):
    @blp.response(200, Specialization_Schema)
    def get(self, specialization_id):
        try:
            return specializations[specialization_id]
        except KeyError:
            abort(404, message="Specialization not found.")

    def delete(self, specialization_id):
        try:
            del specializations[specialization_id]
            return {"message": "Specialization deleted."}
        except KeyError:
            abort(404, message="Specialization not found.")


@blp.route("/specialization")
class SpecializationList(MethodView):
    @blp.response(200, Specialization_Schema(many=True))
    def get(self):
        return {"specializations": list(specializations.values())}


    @blp.arguments(Specialization_Schema)
    @blp.response(200, Specialization_Schema)
    def post(self, specialization_data):
        '''
        specialization_data = request.get_json()
        if "name" not in specialization_data:
            abort(
                400,
                message="Bad request. Ensure 'name' is included in the JSON payload.",
           )
       '''
        for specialization in specializations.values():
            if specialization_data["name"] == specialization["name"]:
                abort(400, message="Specialization already exists.")

        specialization_id = uuid.uuid4().hex
        specialization = {**specialization_data, "specialization_id": specialization_id}
        specializations[specialization_id] = specialization

        return specialization