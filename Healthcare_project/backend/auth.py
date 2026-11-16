from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from database import create_user, verify_user

auth_bp = Blueprint("auth", __name__)


def _data():
    return request.get_json(silent=True) or {}


@auth_bp.post("/register")
def register():
    data = _data()
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not name or not email or not password:
        return jsonify({"success": False, "message": "All fields are required."}), 400
    if len(password) < 6:
        return jsonify({"success": False, "message": "Password must contain at least 6 characters."}), 400

    user_id = create_user(name, email, password)
    if user_id is None:
        return jsonify({"success": False, "message": "An account with this email already exists."}), 409

    token = create_access_token(identity=str(user_id))
    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "token": token,
        "user": {"id": user_id, "name": name, "email": email},
    }), 201


@auth_bp.post("/login")
def login():
    data = _data()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    user = verify_user(email, password)

    if user is None:
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    token = create_access_token(identity=str(user["id"]))
    return jsonify({
        "success": True,
        "message": "Login successful.",
        "token": token,
        "user": {"id": user["id"], "name": user["name"], "email": user["email"]},
    })
