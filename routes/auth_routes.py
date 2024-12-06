from flask import Blueprint, request, jsonify, session
from utils.db_connection import get_db
from bson import ObjectId, json_util
import json

auth = Blueprint('auth', __name__)
db = get_db()
users = db.users

def parse_json(data):
    return json.loads(json_util.dumps(data))

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = users.find_one({"user_id": data["user_id"], "password": data["password"]})
    if user:
        user['_id'] = str(user['_id'])
        session['user'] = user
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out"}), 200

# Create a new user
@auth.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data.get("user_id") or not data.get("password"):
        return jsonify({"message": "User ID and Password are required"}), 400

    if users.find_one({"user_id": data["user_id"]}):
        return jsonify({"message": "User ID already exists"}), 409

    new_user = {
        "user_id": data["user_id"],
        "password": data["password"],
        "name": data.get("name", ""),
        "email": data.get("email", ""),
        "role": data.get("role", "user")  # Default role is 'user'
    }
    result = users.insert_one(new_user)
    return jsonify({"message": "User created successfully", "user_id": str(result.inserted_id)}), 201

# Edit an existing user
@auth.route('/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
    data = request.json
    update_data = {}
    if "password" in data:
        update_data["password"] = data["password"]
    if "name" in data:
        update_data["name"] = data["name"]
    if "email" in data:
        update_data["email"] = data["email"]
    if "role" in data:
        update_data["role"] = data["role"]

    result = users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.matched_count == 0:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"message": "User updated successfully"}), 200

# Delete a user
@auth.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200