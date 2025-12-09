from flask_smorest import Blueprint, abort
from models.users import Users
from flask.views import MethodView
from schemas import UserLoginSchema, UserRegisterSchema, TokenSchema
from models.users import Users
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token





blp = Blueprint("Users", __name__, description="Users")


@blp.route("/register")
class User(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserRegisterSchema)
    def post(self, user_data):
        existing = Users.query.filter_by(username=user_data.get("username")).first()
        if existing:
            abort(400, message="User already exists")
        role = user_data.get("role", "").capitalize()
        if role not in ["Admin", "Student", "Head"]:
            abort(400, message="Invalid role")
        hashed_password = generate_password_hash(user_data["password"], method="pbkdf2:sha256", salt_length=8)
        user_data["password"] = hashed_password
        user = Users(**user_data)
        db.session.add(user)
        db.session.commit()
        return user

@blp.route("/register")
class User(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserRegisterSchema)
    def post(self, user_data):
        existing = Users.query.filter_by(username=user_data.get("username")).first()
        if existing:
            abort(400, message="User already exists")
        role = user_data.get("role", "").capitalize()
        if role not in ["Admin", "Student", "Head"]:
            abort(400, message="Invalid role")
        hashed_password = generate_password_hash(user_data["password"], method="pbkdf2:sha256", salt_length=8)
        user_data["password"] = hashed_password
        user = Users(**user_data)
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/login")
class UserLog(MethodView):
    @blp.arguments(UserLoginSchema)
    @blp.response(200, TokenSchema)
    def post(self, user_data):
        existing = Users.query.filter_by(username=user_data.get("username")).first()
        if not existing:
            abort(404, message="User not found")
        if not check_password_hash(existing.password, user_data["password"]):
            abort(401, message="Invalid password")
        access_token = create_access_token(
            identity=str(existing.id),  
            additional_claims={"role": existing.role}
        )
        return {"access_token":access_token}

