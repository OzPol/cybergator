from flask import Blueprint, request, jsonify, session
from app.services.auth_service import signup, login, delete_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup_route():
    """User signup"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    response = signup(username, password)

    if isinstance(response, dict) and "error" in response:
        return jsonify(response), 400

    return jsonify(response.to_dict()), 201

@auth_bp.route("/login", methods=["POST"])
def login_route():
    """User login"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    if "user" in session:
        return jsonify({"message": "you are already logged in."}), 400

    response = login(username, password)

    if "error" in response:
        return jsonify(response), 401
    
    session["user"] = username

    return jsonify(response), 200

@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    """Returns the logged-in user's session info"""
    user = session.get("user")
    if user:
        return jsonify({"username": user}), 200
    return jsonify({"error": "User not logged in"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    """User logout"""
    if "user" in session:
        session.pop("user")
        return jsonify({"message": "Logout successful"}), 200
    return jsonify({"error": "User not logged in"}), 401

@auth_bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    """Delete user by ID"""
    response = delete_user(user_id)
    if "error" in response:
        return jsonify(response), 404
    return jsonify(response), 200
