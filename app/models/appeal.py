"""
Appeal model for class change requests.
"""
from app.extensions import db
from datetime import datetime

class ClassAppeal(db.Model):
    """Model for tracking class change appeals."""
    __tablename__ = 'class_appeals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chad_id = db.Column(db.Integer, db.ForeignKey('chads.id'), nullable=False)
    
    # Appeal details
    current_class = db.Column(db.String(50), nullable=False)
    requested_class = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.String(20), nullable=False)
    contributions = db.Column(db.Text, nullable=False)
    evidence = db.Column(db.Text, nullable=False)
    
    # Appeal status
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reviewer_notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='class_appeals')
    chad = db.relationship('Chad', backref='class_appeals')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='reviewed_appeals')
    
    def __repr__(self):
        return f'<ClassAppeal {self.id}: {self.current_class} → {self.requested_class} ({self.status})>'
    
    def approve(self, reviewer_id, notes=None):
        """Approve the appeal and update the chad's class."""
        from app.models.chad import ChadClass
        
        # Find the requested class
        blockchain_detective = ChadClass.query.filter_by(name='Blockchain Detective').first()
        if not blockchain_detective:
            return False, "Requested class not found"
        
        try:
            # Update the chad's class
            self.chad.class_id = blockchain_detective.id
            
            # Update appeal status
            self.status = 'approved'
            self.reviewer_id = reviewer_id
            self.reviewer_notes = notes
            self.reviewed_at = datetime.utcnow()
            
            # Commit changes
            db.session.commit()
            
            return True, "Appeal approved successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def reject(self, reviewer_id, notes=None):
        """Reject the appeal."""
        try:
            # Update appeal status
            self.status = 'rejected'
            self.reviewer_id = reviewer_id
            self.reviewer_notes = notes
            self.reviewed_at = datetime.utcnow()
            
            # Commit changes
            db.session.commit()
            
            return True, "Appeal rejected successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e) 