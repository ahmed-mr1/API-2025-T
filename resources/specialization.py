from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from schemas import Specialization_Schema, PlainSpecialization_Schema
from models.specialization import SpecializationModel
from flask_jwt_extended import jwt_required, get_jwt



blp = Blueprint("specializations", __name__, description="Operations on specializations")



@blp.route("/specialization/<string:specialization_id>")
class Specialization(MethodView):
    @blp.response(200, Specialization_Schema)
    @jwt_required()
    def get(self, specialization_id):
        specialization = SpecializationModel.query.filter_by(specialization_id=specialization_id).first()
        if not specialization:
            abort(404, message="Specialization not found.")
        return specialization

    @blp.response(200)
    @jwt_required()
    def delete(self, specialization_id):
        claims = get_jwt()
        role = claims["role"]
        if role != "Admin":
            abort(403, message="Admins only can delete specializations")
        specialization = SpecializationModel.query.filter_by(specialization_id=specialization_id).first()
        if not specialization:
            abort(404, message="Specialization not found.")
        db.session.delete(specialization)
        db.session.commit()
        return {"message": "Specialization deleted."}

    @blp.arguments(PlainSpecialization_Schema)
    @blp.response(200, Specialization_Schema)
    @jwt_required()
    def put(self, specialization_data, specialization_id):
        claims = get_jwt()
        role = claims["role"]
        if role != "Admin":
            abort(403, message="Admins only can delete specializations")
        specialization = SpecializationModel.query.filter_by(specialization_id=specialization_id).first()
        if not specialization:
            abort(404, message="Specialization not found.")

        # Prevent updating the UUID identifier
        if "specialization_id" in specialization_data:
            del specialization_data["specialization_id"]

        for key, value in specialization_data.items():
            setattr(specialization, key, value)

        db.session.commit()
        return specialization


@blp.route("/specialization")
class SpecializationList(MethodView):
    @blp.response(200, Specialization_Schema(many=True))
    @jwt_required()
    def get(self):
        return SpecializationModel.query.all()


    @blp.arguments(Specialization_Schema)
    @blp.response(201, Specialization_Schema)
    @jwt_required()
    def post(self, specialization_data):
        claims = get_jwt()
        role = claims["role"]
        if role != "Admin":
            abort(403, message="Admins only can delete specializations")
        existing = SpecializationModel.query.filter_by(name=specialization_data.get("name")).first()
        if existing:
            abort(400, message="Specialization already exists.")

        specialization = SpecializationModel(**specialization_data)
        db.session.add(specialization)
        db.session.commit()
        return specialization