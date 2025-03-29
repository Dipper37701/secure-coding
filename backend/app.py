# backend/app.py
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
import os

from config import Config
from models import db
from routes import register_routes
from sockets import register_socket_events

# Create the uploads directory if it doesn't exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config["JWT_VERIFY_SUB"] = False
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Register blueprints
    register_routes(app)
    
    # Register socket events
    register_socket_events(socketio)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app, socketio

app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)