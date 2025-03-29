# backend/utils/auth.py
import bcrypt
from flask_jwt_extended import create_access_token

def hash_password(password):
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password, password):
    """Check if a password matches the hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id):
    """Generate a JWT token for a user."""
    return create_access_token(identity=user_id)