# backend/models/report.py
from . import db, datetime

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    reason = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Report {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'reporter_id': self.reporter_id,
            'target_id': self.target_id,
            'product_id': self.product_id,
            'reason': self.reason,
            'created_at': self.created_at.isoformat()  # ISO 형식 문자열로 변환
        }