from flask import request, jsonify
from services.auth_service import authenticate_user, generate_token, get_user_from_token

def login_controller():
    data = request.get_json()
    user = authenticate_user(data.get('username'), data.get('password'))

    if user:
        return jsonify({'token': generate_token(user)})
    return jsonify({'message': 'Invalid credentials'}), 401

def profile_controller():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Token is missing"}), 403

    token = auth_header.split(" ")[1]

    try:
        user = get_user_from_token(token)
        if user:
            return jsonify({
                "username": user.username,
                "email": user.email,
                "user_id": str(user.id)
            })
        return jsonify({"message": "User not found"}), 404
    except ValueError as e:
        return jsonify({"message": str(e)}), 401