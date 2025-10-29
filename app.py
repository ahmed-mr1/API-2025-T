from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:<YOUR_PASSWORD>@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

specializations = [
    {
        "name": "IT",
        "course_items": [{"name": "Web Services", "Type": "Mandatory"}]
    }
]

@app.get("/specialization")
def get_specializations():
    return {"specializations": specializations}

@app.post("/specialization")
def create_specializations():
    request_data=request.get_json()
    new_specialization={"name": request_data["name"], "course_items":[]}
    specializations.append(new_specialization)
    return new_specialization, 201


@app.post("/specialization/<string:name>/course_item")
def create_course_item(name):
    request_data=request.get_json()
    for specialization in specializations:
        if specialization["name"]==name:
            new_course_item={"name": request_data["name"], "type": request_data["type"]}
            specialization["course_items"].append(new_course_item)
            return new_course_item, 201
    return{"message":"Specialization not found"}, 404
    

@app.get("/specialization/<string:name>")
def get_specialization(name):
    for specialization in specializations:
        if specialization["name"] == name:
            return {"specialization": specialization}
    return{"message":"Specialization not found"}, 404
    

@app.get("/specialization/<string:name>/course_item")
def get_course_item(name):
    for specialization in specializations:
        if specialization["name"] == name:
            return {"course_items":specialization["course_items"]}
    return{"message":"Specialization not found"}, 404

@app.put("/specialization/<string:name>")
def update_specialization(name):
    request_data = request.get_json()
    for specialization in specializations:
        if specialization["name"] == name:
            specialization["name"] = request_data["name"]
            return specialization
    return {"message":"Specalization not found"}, 404

@app.delete("/specialization/<string:name>")
def delete_specialization(name):
    for specialization in specializations:
        if specialization["name"] == name:
            specializations.remove(specialization)
            return {"message": "Specialization deleted"}
    return {"message":"Specalization not found"}, 404

@app.delete("/specialization/<string:specialization_name>/<string:course_name>")
def delete_course_item(specialization_name,course_name):
    for specialization in specializations:
        if specialization["name"] == specialization_name:
            for course in specialization["course_items"]:
                if course["name"] == course_name:
                    specialization["course_items"].remove(course)
                    return {"message":"Course item deleted"}
            return {"message":"Course not found"}, 404
    return {"message":"Specialization not found"}, 404
                