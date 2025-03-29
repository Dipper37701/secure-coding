# backend/routes/__init__.py
from flask import Blueprint

def register_routes(app):
    # Import routes
    from .auth import auth_bp
    from .user import user_bp
    from .product import product_bp
    from .chat import chat_bp
    from .report import report_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(chat_bp, url_prefix='/api/chats')
    app.register_blueprint(report_bp, url_prefix='/api/reports')