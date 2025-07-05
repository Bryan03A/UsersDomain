import jwt
import datetime
from flask import current_app
from models.user_model import User, db
from services.password_service import hash_password
from events.publisher import publish_event

def generate_token(user: User) -> str:
    payload = {
        'user_id': str(user.id),
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def authenticate_user(username_or_email: str, password: str):
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if user and user.password == hash_password(password):
        publish_event("UserLoggedIn", {
            "user_id": str(user.id),
            "username": user.username
        })
        return user
    return None

def get_user_from_token(token: str):
    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return User.query.get(decoded['user_id'])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")