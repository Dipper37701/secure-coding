# backend/models/chat.py
from datetime import datetime
from . import db

class ChatRoom(db.Model):
    __tablename__ = 'chat_rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)  # For group chats
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatRoom {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_private': self.is_private,
            'created_at': self.created_at.isoformat(),  # 날짜를 ISO 형식 문자열로 변환
            'participants': [p.user.username for p in self.participants]
        }

class ChatParticipant(db.Model):
    __tablename__ = 'chat_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate participants
    __table_args__ = (db.UniqueConstraint('room_id', 'user_id', name='uix_participant'),)
    
    # Define relationships
    room = db.relationship('ChatRoom', backref=db.backref('participants', lazy=True))
    user = db.relationship('User', backref=db.backref('chat_participations', lazy=True))

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define relationships
    room = db.relationship('ChatRoom', backref=db.backref('messages', lazy=True))
    sender = db.relationship('User', backref=db.backref('messages_sent', lazy=True))
    
    def __repr__(self):
        return f'<ChatMessage {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.username,
            'content': self.content,
            'created_at': self.created_at.isoformat()  # 날짜를 ISO 형식 문자열로 변환
        }