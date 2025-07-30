from flask import Blueprint, request, jsonify
from app import db
from models import Plant

plant_bp = Blueprint("plants", __name__)

@plant_bp.route("/plants", methods=["GET"])
def get_plants():
    plants = Plant.query.all()
    return jsonify([plant.to_dict() for plant in plants]), 200

@plant_bp.route("/plants/<int:id>", methods=["GET"])
def get_plant(id):
    plant = db.session.get(Plant, id)
    if plant:
        return jsonify(plant.to_dict()), 200
    return {"error": "Plant not found"}, 404

@plant_bp.route("/plants", methods=["POST"])
def create_plant():
    data = request.get_json()
    new_plant = Plant(
        name=data["name"],
        image=data["image"],
        price=data["price"],
        is_in_stock=data.get("is_in_stock", True),
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify(new_plant.to_dict()), 201

@plant_bp.route("/plants/<int:id>", methods=["PATCH"])
def update_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return {"error": "Plant not found"}, 404

    data = request.get_json()
    for attr in data:
        setattr(plant, attr, data[attr])
    db.session.commit()
    return jsonify(plant.to_dict()), 200

@plant_bp.route("/plants/<int:id>", methods=["DELETE"])
def delete_plant(id):
    plant = db.session.get(Plant, id)
    if not plant:
        return {"error": "Plant not found"}, 404

    db.session.delete(plant)
    db.session.commit()
    return {}, 204
