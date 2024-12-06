from flask import Blueprint, request, jsonify, session
from utils.db_connection import get_db
from utils.login_required import login_required
from models.task_model import task_schema
from bson import ObjectId, json_util  # Import ObjectId
import json

tasks_bp = Blueprint('tasks', __name__)
db = get_db()
tasks = db.tasks

def parse_json(data):
    return json.loads(json_util.dumps(data))

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = task_schema(data)
    tasks.insert_one(task)
    return jsonify({"message": "Task created successfully"}), 201

@tasks_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    tasks.update_one({"_id": ObjectId(task_id)}, {"$set": data})
    return jsonify({"message": "Task updated successfully"}), 200

@tasks_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks.delete_one({"_id": ObjectId(task_id)})
    return jsonify({"message": "Task deleted successfully"}), 200

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    filters = request.args.to_dict()
    task_list = list(tasks.find(filters))
    return jsonify(parse_json(task_list)), 200

