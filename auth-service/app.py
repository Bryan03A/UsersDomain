from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import jwt
import datetime
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

# ───────────── Models ─────────────
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# ──────── Utility Functions ────────
def hash_password(password: str) -> str:
    salt = 'salt'
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 1000, 64).hex()

def generate_token(user) -> str:
    payload = {
        'user_id': str(user.id),
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# ───────────── Endpoints ─────────────
@app.route('/auth/health', methods=['GET'])
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        result = db.session.execute(text("SELECT NOW()")).fetchone()
        return jsonify({"message": "Successful connection", "timestamp": str(result[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter(
        (User.username == data.get('username')) | (User.email == data.get('username'))
    ).first()

    if user and hash_password(data.get('password')) == user.password:
        return jsonify({'token': generate_token(user)})
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/profile', methods=['GET'])
def profile():
    header = request.headers.get('Authorization')
    if not header or not header.startswith("Bearer "):
        return jsonify({"message": "Token is missing"}), 403

    try:
        token = header.split(" ")[1]
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = db.session.get(User, decoded['user_id'])

        if user:
            return jsonify({
                "username": user.username,
                "email": user.email,
                "user_id": user.id
            })
        return jsonify({"message": "User not found"}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

# ───────────── Entrypoint ─────────────
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)