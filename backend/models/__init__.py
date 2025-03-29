# backend/models/__init__.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from .user import User
from .product import Product
from .report import Report
from .chat import ChatRoom, ChatParticipant, ChatMessage

# Export models
__all__ = ['db', 'User', 'Product', 'Report', 'ChatRoom', 'ChatParticipant', 'ChatMessage']