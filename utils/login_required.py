from functools import wraps
from flask import request, jsonify, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"message": "Unauthorized: Please log in first"}), 401
        return f(*args, **kwargs)
    return decorated_function