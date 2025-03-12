"""
Cabal analytics model for tracking metrics over time.

This module provides a model for tracking various metrics about cabals over time,
which can be used for analytics dashboards and trend analysis.
"""

from app import db
from datetime import datetime
import uuid

class CabalAnalytics(db.Model):
    """
    Model for tracking cabal metrics over time.
    
    Attributes:
        id (str): Unique identifier for the analytics record
        cabal_id (str): ID of the cabal being tracked
        timestamp (datetime): When this analytics snapshot was taken
        member_count (int): Number of members in the cabal at this time
        total_power (float): Total power of the cabal at this time
        rank (int): Rank on the leaderboard at this time
        battles_won (int): Cumulative battles won at this time
        battles_lost (int): Cumulative battles lost at this time
        referrals (int): Cumulative referrals at this time
    """
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cabal_id = db.Column(db.String(36), db.ForeignKey('cabal.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Membership metrics
    member_count = db.Column(db.Integer, nullable=False)
    active_member_count = db.Column(db.Integer, nullable=False)
    
    # Performance metrics
    total_power = db.Column(db.Float, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    
    # Battle metrics
    battles_won = db.Column(db.Integer, nullable=False)
    battles_lost = db.Column(db.Integer, nullable=False)
    
    # Engagement metrics
    referrals = db.Column(db.Integer, nullable=False)
    
    # Relationships
    cabal = db.relationship('Cabal', backref='analytics_history')
    
    def __repr__(self):
        """String representation of the analytics record."""
        return f'<CabalAnalytics for {self.cabal_id} at {self.timestamp}>'
    
    @classmethod
    def create_snapshot(cls, cabal_id):
        """
        Create a snapshot of cabal metrics for the given cabal.
        
        Args:
            cabal_id (str): The ID of the cabal to create a snapshot for
            
        Returns:
            CabalAnalytics: The created analytics record
        """
        from app.models.cabal import Cabal, CabalMember
        from app.models.referral import Referral
        
        cabal = Cabal.query.get(cabal_id)
        if not cabal:
            return None
        
        # Get current metrics
        member_count = CabalMember.query.filter_by(cabal_id=cabal_id).count()
        active_member_count = CabalMember.query.filter_by(cabal_id=cabal_id, is_active=True).count()
        referral_count = Referral.query.filter_by(cabal_id=cabal_id).count()
        
        # Create analytics record
        analytics = cls(
            cabal_id=cabal_id,
            member_count=member_count,
            active_member_count=active_member_count,
            total_power=cabal.total_power,
            rank=cabal.rank or 0,
            battles_won=cabal.battles_won,
            battles_lost=cabal.battles_lost,
            referrals=referral_count
        )
        
        db.session.add(analytics)
        db.session.commit()
        
        return analytics
    
    @classmethod
    def get_history(cls, cabal_id, days=30):
        """
        Get historical analytics data for a cabal.
        
        Args:
            cabal_id (str): The ID of the cabal to get history for
            days (int): Number of days of history to retrieve
            
        Returns:
            list: CabalAnalytics records for the specified period
        """
        cutoff_date = datetime.utcnow() - datetime.timedelta(days=days)
        
        return cls.query.filter(
            cls.cabal_id == cabal_id,
            cls.timestamp >= cutoff_date
        ).order_by(cls.timestamp).all()
    
    @classmethod
    def get_latest(cls, cabal_id):
        """
        Get the most recent analytics snapshot for a cabal.
        
        Args:
            cabal_id (str): The ID of the cabal to get data for
            
        Returns:
            CabalAnalytics: The most recent analytics record
        """
        return cls.query.filter_by(cabal_id=cabal_id).order_by(
            cls.timestamp.desc()
        ).first() 