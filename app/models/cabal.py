"""
Cabal model for Chad Battles.
"""
from app.extensions import db
from datetime import datetime
import enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
import uuid

class CabalMemberRole(enum.Enum):
    """Enum for cabal member roles."""
    LEADER = "leader"
    OFFICER = "officer"
    MEMBER = "member"
    RECRUIT = "recruit"

class Cabal(db.Model):
    """Cabal model for groups of users"""
    __tablename__ = 'cabals'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    logo_url = Column(String(255), nullable=True)
    
    # Cabal stats
    total_power = Column(Float, nullable=False, default=0)
    member_count = Column(Integer, nullable=False, default=0)
    victory_count = Column(Integer, nullable=False, default=0)
    defeat_count = Column(Integer, nullable=False, default=0)
    
    # Cabal status
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Cabal leadership
    leader_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationships
    leader = relationship('User', foreign_keys=[leader_id], backref='led_cabals')
    members = relationship('CabalMember', back_populates='cabal', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cabal {self.id}: {self.name}>'
    
    def calculate_total_power(self):
        """Calculate the total power of the cabal based on members"""
        # This is a simplified version for deployment
        # In the full version, we would calculate based on member stats
        total = 0
        for member in self.members:
            if member.is_active:
                total += member.power_contribution
        self.total_power = total
        return self.total_power
    
    def update_member_count(self):
        """Update the member count"""
        self.member_count = sum(1 for member in self.members if member.is_active)
        return self.member_count
    
    def add_member(self, user, role='member'):
        """Add a user to the cabal"""
        from app.models.cabal_member import CabalMember
        
        # Check if user is already a member
        existing_member = CabalMember.query.filter_by(cabal_id=self.id, user_id=user.id).first()
        if existing_member:
            if existing_member.is_active:
                return False, "User is already a member of this cabal"
            else:
                existing_member.is_active = True
                existing_member.role = role
                db.session.commit()
                self.update_member_count()
                return True, "User rejoined the cabal"
        
        # Create new member
        member = CabalMember(
            cabal_id=self.id,
            user_id=user.id,
            role=role,
            joined_at=datetime.utcnow()
        )
        db.session.add(member)
        db.session.commit()
        
        # Update cabal stats
        self.update_member_count()
        self.calculate_total_power()
        db.session.commit()
        
        return True, "User added to cabal"
    
    def remove_member(self, user_id):
        """Remove a user from the cabal"""
        from app.models.cabal_member import CabalMember
        
        member = CabalMember.query.filter_by(cabal_id=self.id, user_id=user_id, is_active=True).first()
        if not member:
            return False, "User is not a member of this cabal"
        
        # Cannot remove the leader
        if user_id == self.leader_id:
            return False, "Cannot remove the cabal leader"
        
        member.is_active = False
        member.left_at = datetime.utcnow()
        db.session.commit()
        
        # Update cabal stats
        self.update_member_count()
        self.calculate_total_power()
        db.session.commit()
        
        return True, "User removed from cabal"

    @property
    def member_count(self):
        """Get the number of members in the cabal"""
        return len(self.members)
    
    @property
    def total_power(self):
        """Get the total power of all members in the cabal"""
        return sum([member.power_contribution for member in self.members if member.is_active])
    
    @classmethod
    def get_top_cabals(cls, limit=10):
        """
        Get the top cabals for the leaderboard
        
        Returns:
            list: List of tuples (cabal_id, cabal_name, member_count, total_power)
        """
        try:
            cabals = cls.query.all()
            
            # Calculate stats for each cabal
            cabal_stats = []
            for cabal in cabals:
                members = cabal.members
                member_count = len(members)
                
                if member_count == 0:
                    continue
                    
                # Calculate total power (this is just an example, adjust as needed)
                total_power = 0
                for membership in members:
                    if membership.is_active:
                        total_power += membership.power_contribution
                
                cabal_stats.append((
                    cabal.id,
                    cabal.name,
                    member_count,
                    total_power
                ))
            
            # Sort by total power descending
            cabal_stats.sort(key=lambda x: x[3], reverse=True)
            
            # Return top cabals
            return cabal_stats[:limit]
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting top cabals: {str(e)}")
            return []

class CabalMember(db.Model):
    """Model for cabal membership"""
    __tablename__ = 'cabal_members'
    
    id = Column(Integer, primary_key=True)
    cabal_id = Column(Integer, ForeignKey('cabals.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Member status
    role = Column(String(20), nullable=False, default='member')
    is_active = Column(Boolean, nullable=False, default=True)
    power_contribution = Column(Float, nullable=False, default=0)
    
    # Timestamps
    joined_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    left_at = Column(DateTime, nullable=True)
    
    # Relationships
    cabal = relationship('Cabal', back_populates='members')
    user = relationship('User', backref='cabal_memberships')
    
    def __repr__(self):
        return f'<CabalMember {self.id}: {self.user_id} in {self.cabal_id}>'
    
    def calculate_power_contribution(self):
        """Calculate the power contribution of this member"""
        # This is a simplified version for deployment
        # In the full version, we would calculate based on user stats
        self.power_contribution = 100  # Placeholder
        return self.power_contribution

# Simple stub implementation of CabalBattle to resolve import errors
class CabalBattle:
    """
    Stub implementation of CabalBattle for deployment.
    This class is included to resolve import errors but is not fully implemented.
    """
    
    @classmethod
    def query(cls):
        """Return a query-like object with filter_by method that always returns empty results."""
        class StubQuery:
            def filter_by(self, **kwargs):
                return self
                
            def filter(self, *args):
                return self
                
            def order_by(self, *args):
                return self
                
            def limit(self, n):
                return []
                
            def all(self):
                return []
                
            def first(self):
                return None
                
            def count(self):
                return 0
                
            def get_or_404(self, id):
                from flask import abort
                abort(404)
        
        return StubQuery()
    
    @staticmethod
    def get_current_week_number():
        """Get the current week number."""
        return datetime.utcnow().isocalendar()[1]
    
    @classmethod
    def count_battles_this_week(cls, cabal_id):
        """Get the count of battles this week."""
        return 0

# Simple stub for CabalBattleParticipant
class CabalBattleParticipant:
    """
    Stub implementation of CabalBattleParticipant for deployment.
    """
    
    @classmethod
    def query(cls):
        """Return a query-like object that always returns empty results."""
        class StubQuery:
            def filter_by(self, **kwargs):
                return self
                
            def first(self):
                return None
        
        return StubQuery()

# Additional class stubs for other missing classes referenced in imports
class CabalOfficerRole:
    """Stub for CabalOfficerRole."""
    pass

class CabalVote:
    """Stub for CabalVote."""
    pass

class CabalMembership(db.Model):
    """
    Model for tracking cabal memberships
    """
    id = Column(Integer, primary_key=True)
    cabal_id = Column(Integer, ForeignKey('cabals.id'), nullable=False)
    chad_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role = Column(String(50), nullable=False, default='member')
    joined_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    cabal = relationship('Cabal', back_populates='members')
    chad = relationship('User', backref='cabal_memberships')
    
    def __repr__(self):
        return f'<CabalMembership {self.id}: {self.chad_id} in {self.cabal_id}>' 