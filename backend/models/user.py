# backend/models/user.py
from . import db, datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    report_count = db.Column(db.Integer, default=0)
    
    # Relationships
    products = db.relationship('Product', backref='seller', lazy=True)
    sent_reports = db.relationship('Report', foreign_keys='Report.reporter_id', backref='reporter', lazy=True)
    received_reports = db.relationship('Report', foreign_keys='Report.target_id', backref='target', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'description': self.description,
            'created_at': self.created_at.isoformat(),  # ISO 형식 문자열로 변환
            'is_active': self.is_active
        }