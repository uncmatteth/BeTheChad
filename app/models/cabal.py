"""
Cabal model for Chad Battles.
"""
from app.extensions import db
from datetime import datetime
import enum

class CabalMemberRole(enum.Enum):
    """Enum for cabal member roles."""
    LEADER = "leader"
    OFFICER = "officer"
    MEMBER = "member"
    RECRUIT = "recruit"

class Cabal(db.Model):
    """Cabal model for player guilds/clans."""
    __tablename__ = 'cabals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Cabal stats
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    chadcoin_balance = db.Column(db.Integer, default=0)
    
    # Cabal customization
    logo_url = db.Column(db.String(255), nullable=True)
    banner_url = db.Column(db.String(255), nullable=True)
    color_scheme = db.Column(db.String(20), default="default")
    
    # Cabal metrics
    battles_won = db.Column(db.Integer, default=0)
    battles_lost = db.Column(db.Integer, default=0)
    total_member_count = db.Column(db.Integer, default=1)  # Start with leader
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    leader = db.relationship('User', backref=db.backref('led_cabal', uselist=False))
    members = db.relationship('CabalMember', backref='cabal', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cabal {self.name} (Level {self.level})>'
    
    def add_member(self, user_id, role=CabalMemberRole.RECRUIT.value):
        """Add a new member to the cabal.
        
        Args:
            user_id (int): The user ID to add
            role (str): The role to assign
        
        Returns:
            CabalMember: The new member or None if already in cabal
        """
        # Check if user is already in the cabal
        existing_member = CabalMember.query.filter_by(cabal_id=self.id, user_id=user_id).first()
        if existing_member:
            return None
        
        # Add the new member
        member = CabalMember(
            cabal_id=self.id,
            user_id=user_id,
            role=role
        )
        
        db.session.add(member)
        self.total_member_count += 1
        db.session.commit()
        
        return member
    
    def remove_member(self, user_id):
        """Remove a member from the cabal.
        
        Args:
            user_id (int): The user ID to remove
        
        Returns:
            bool: True if removed, False otherwise
        """
        # Cannot remove the leader
        if user_id == self.leader_id:
            return False
        
        # Find and remove the member
        member = CabalMember.query.filter_by(cabal_id=self.id, user_id=user_id).first()
        if member:
            db.session.delete(member)
            self.total_member_count -= 1
            db.session.commit()
            return True
        
        return False
    
    def change_leader(self, new_leader_id):
        """Change the leader of the cabal.
        
        Args:
            new_leader_id (int): The new leader's user ID
        
        Returns:
            bool: True if changed, False otherwise
        """
        # Check if the new leader is a member
        member = CabalMember.query.filter_by(cabal_id=self.id, user_id=new_leader_id).first()
        if not member:
            return False
        
        # Update the old leader's role
        old_leader_member = CabalMember.query.filter_by(cabal_id=self.id, user_id=self.leader_id).first()
        if old_leader_member:
            old_leader_member.role = CabalMemberRole.MEMBER.value
        
        # Update the new leader's role
        member.role = CabalMemberRole.LEADER.value
        
        # Update the cabal
        self.leader_id = new_leader_id
        db.session.commit()
        
        return True
    
    def add_xp(self, amount):
        """Add XP to the cabal and level up if necessary."""
        if amount <= 0:
            return False
        
        self.xp += amount
        
        # Check for level up
        xp_needed = self.get_xp_for_next_level()
        while self.xp >= xp_needed:
            self.level_up()
            xp_needed = self.get_xp_for_next_level()
        
        db.session.commit()
        return True
    
    def level_up(self):
        """Level up the cabal."""
        self.level += 1
        return True
    
    def get_xp_for_next_level(self):
        """Calculate XP needed for the next level."""
        return 1000 * self.level + 500 * (self.level - 1) ** 2
    
    def add_chadcoin(self, amount):
        """Add chadcoin to the cabal treasury.
        
        Args:
            amount (int): The amount to add
        
        Returns:
            bool: True if added, False otherwise
        """
        if amount <= 0:
            return False
        
        self.chadcoin_balance += amount
        db.session.commit()
        
        return True
    
    def remove_chadcoin(self, amount):
        """Remove chadcoin from the cabal treasury.
        
        Args:
            amount (int): The amount to remove
        
        Returns:
            bool: True if removed, False otherwise
        """
        if amount <= 0 or amount > self.chadcoin_balance:
            return False
        
        self.chadcoin_balance -= amount
        db.session.commit()
        
        return True
    
    def get_active_members(self):
        """Get active members of the cabal."""
        return CabalMember.query.filter_by(cabal_id=self.id, is_active=True).all()
    
    def get_active_member_count(self):
        """Get count of active members."""
        return CabalMember.query.filter_by(cabal_id=self.id, is_active=True).count()
    
    def calculate_total_power(self):
        """Calculate the total power of all members' Chads."""
        total_power = 0
        
        active_members = self.get_active_members()
        for member in active_members:
            # Get the member's Chad
            from app.models.chad import Chad
            chad = Chad.query.filter_by(user_id=member.user_id).first()
            if chad:
                # Get the Chad's total stats
                stats = chad.get_total_stats()
                
                # Calculate power as sum of stats
                power = stats.clout + stats.roast_level + stats.cringe_resistance + stats.drip_factor
                total_power += power
        
        return total_power
    
    @classmethod
    def get_top_cabals(cls, limit=10):
        """Get the top cabals by level."""
        return cls.query.order_by(cls.level.desc(), cls.xp.desc()).limit(limit).all()

class CabalMember(db.Model):
    """Cabal member model for tracking cabal membership."""
    __tablename__ = 'cabal_members'
    
    id = db.Column(db.Integer, primary_key=True)
    cabal_id = db.Column(db.Integer, db.ForeignKey('cabals.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20), default=CabalMemberRole.RECRUIT.value)
    
    # Member stats
    contribution_points = db.Column(db.Integer, default=0)
    battles_participated = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('cabal_membership', uselist=False))
    
    def __repr__(self):
        return f'<CabalMember {self.user_id} in {self.cabal_id} as {self.role}>'
    
    def add_contribution_points(self, amount):
        """Add contribution points for cabal activities."""
        if amount <= 0:
            return False
        
        self.contribution_points += amount
        db.session.commit()
        
        return True
    
    def increment_battles_participated(self):
        """Increment the battles participated count."""
        self.battles_participated += 1
        db.session.commit()
        
        return True
    
    def update_activity(self):
        """Update the last active timestamp."""
        self.last_active_at = datetime.utcnow()
        db.session.commit()
        
        return True

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