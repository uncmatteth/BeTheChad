"""
Appeal model for class change requests.
"""
from app.extensions import db
from datetime import datetime

class Appeal(db.Model):
    """Model for class appeals"""
    __tablename__ = 'appeals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    requested_class = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    admin_notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='appeals')
    admin = db.relationship('User', foreign_keys=[admin_id], backref='processed_appeals')
    
    def __init__(self, user_id, requested_class, reason):
        self.user_id = user_id
        self.requested_class = requested_class
        self.reason = reason
    
    def approve(self, admin, reason=None):
        """Approve the appeal"""
        if self.status != 'pending':
            raise ValueError('This appeal has already been processed')
            
        self.status = 'approved'
        self.admin_id = admin.id
        self.admin_notes = reason
        self.user.chad_class = self.requested_class
        self.updated_at = datetime.utcnow()
    
    def reject(self, admin, reason=None):
        """Reject the appeal"""
        if self.status != 'pending':
            raise ValueError('This appeal has already been processed')
            
        self.status = 'rejected'
        self.admin_id = admin.id
        self.admin_notes = reason
        self.updated_at = datetime.utcnow()
    
    @property
    def status_badge_class(self):
        """Return Bootstrap badge class based on status"""
        return {
            'pending': 'badge-warning',
            'approved': 'badge-success',
            'rejected': 'badge-danger'
        }.get(self.status, 'badge-secondary')
    
    def __repr__(self):
        return f'<Appeal {self.id}: {self.user.username} -> {self.requested_class} ({self.status})>' 