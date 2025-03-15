from app import db
from datetime import datetime
import uuid

class Referral(db.Model):
    """
    Referral model for tracking cabal member referrals.
    
    Attributes:
        id (str): Unique identifier for the referral
        referrer_id (str): ID of the Chad who referred someone
        referred_id (str): ID of the Chad who was referred
        cabal_id (str): ID of the cabal the referral is for
        created_at (datetime): When the referral was created
    """
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    referrer_id = db.Column(db.String(36), db.ForeignKey('chad.id'), nullable=False)
    referred_id = db.Column(db.String(36), db.ForeignKey('chad.id'), nullable=False)
    cabal_id = db.Column(db.String(36), db.ForeignKey('cabal.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships with explicit primaryjoin conditions
    referrer = db.relationship('Chad', 
                             foreign_keys=[referrer_id],
                             primaryjoin="Referral.referrer_id == Chad.id",
                             backref=db.backref('referrals_made', lazy='dynamic'))
    
    referred = db.relationship('Chad', 
                              foreign_keys=[referred_id],
                              primaryjoin="Referral.referred_id == Chad.id",
                              backref=db.backref('referrals_received', lazy='dynamic'))
    
    cabal = db.relationship('Cabal', backref='referrals')
    
    def __repr__(self):
        """String representation of the referral."""
        return f'<Referral {self.referrer_id} referred {self.referred_id} to {self.cabal_id}>'
    
    @classmethod
    def get_referral_count(cls, referrer_id):
        """
        Get the number of successful referrals made by a user.
        
        Args:
            referrer_id (str): The ID of the referrer Chad
            
        Returns:
            int: The number of successful referrals
        """
        return cls.query.filter_by(referrer_id=referrer_id).count()
    
    @classmethod
    def get_top_referrers(cls, limit=10):
        """
        Get the top referrers by number of successful referrals.
        
        Args:
            limit (int): Maximum number of referrers to return
            
        Returns:
            list: List of tuples (referrer_id, count) sorted by count in descending order
        """
        from sqlalchemy import func
        
        result = db.session.query(
            cls.referrer_id,
            func.count(cls.id).label('referral_count')
        ).group_by(cls.referrer_id).order_by(
            func.count(cls.id).desc()
        ).limit(limit).all()
        
        return result
    
    @classmethod
    def get_cabal_referrals(cls, cabal_id):
        """
        Get all referrals for a specific cabal.
        
        Args:
            cabal_id (str): The ID of the cabal
            
        Returns:
            list: List of Referral objects for the cabal
        """
        return cls.query.filter_by(cabal_id=cabal_id).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def award_milestone_bonus(cls, referrer_id):
        """
        Award bonus for reaching referral milestones.
        
        Args:
            referrer_id (str): The ID of the referrer Chad
            
        Returns:
            tuple: (awarded, amount) where awarded is a boolean indicating if a
                  bonus was awarded, and amount is the bonus amount
        """
        count = cls.get_referral_count(referrer_id)
        
        # Define milestone bonuses
        milestones = {
            5: 250,    # 5 referrals: 250 chadcoin
            10: 500,   # 10 referrals: 500 chadcoin
            25: 1000,  # 25 referrals: 1000 chadcoin
            50: 2500,  # 50 referrals: 2500 chadcoin
            100: 5000  # 100 referrals: 5000 chadcoin
        }
        
        # Check if we've hit a milestone
        for milestone, bonus in milestones.items():
            if count == milestone:
                # Award bonus
                from app.models.chad import Chad
                from app.models.user import User
                from app.models.transaction import Transaction, TransactionType
                
                chad = Chad.query.get(referrer_id)
                if chad:
                    user = User.query.filter_by(chad_id=chad.id).first()
                    if user:
                        Transaction.create(
                            transaction_type=TransactionType.REFERRAL_MILESTONE.value,
                            amount=bonus,
                            to_user_id=user.id,
                            description=f"Milestone bonus for {milestone} successful referrals"
                        )
                        
                        # Share achievement on Twitter
                        try:
                            from app.utils.twitter_api import share_cabal_achievement
                            from app.models.cabal import CabalMember
                            
                            # Get user's cabal
                            member = CabalMember.query.filter_by(chad_id=referrer_id).first()
                            if member and member.cabal:
                                achievement = f"a member who reached {milestone} successful referrals"
                                share_cabal_achievement(
                                    member.cabal.name,
                                    achievement,
                                    user.twitter_handle
                                )
                        except Exception as e:
                            import logging
                            logger = logging.getLogger(__name__)
                            logger.error(f"Error sharing referral milestone: {str(e)}")
                        
                        return True, bonus
        
        return False, 0 