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
        """Add a member to the cabal."""
        # Check if user is already in a cabal
        existing_membership = CabalMember.query.filter_by(user_id=user_id).first()
        if existing_membership:
            return False, "User is already in a cabal"
        
        # Add the member
        member = CabalMember(
            cabal_id=self.id,
            user_id=user_id,
            role=role
        )
        db.session.add(member)
        
        # Update cabal stats
        self.total_member_count += 1
        db.session.commit()
        
        return True, "Member added successfully"
    
    def remove_member(self, user_id):
        """Remove a member from the cabal."""
        # Cannot remove the leader
        if user_id == self.leader_id:
            return False, "Cannot remove the cabal leader"
        
        # Find the member
        member = CabalMember.query.filter_by(cabal_id=self.id, user_id=user_id).first()
        if not member:
            return False, "User is not a member of this cabal"
        
        # Remove the member
        db.session.delete(member)
        
        # Update cabal stats
        self.total_member_count -= 1
        db.session.commit()
        
        return True, "Member removed successfully"
    
    def change_leader(self, new_leader_id):
        """Change the cabal leader."""
        # Check if new leader is a member
        member = CabalMember.query.filter_by(cabal_id=self.id, user_id=new_leader_id).first()
        if not member:
            return False, "New leader must be a cabal member"
        
        # Update the old leader's role
        old_leader = CabalMember.query.filter_by(cabal_id=self.id, user_id=self.leader_id).first()
        if old_leader:
            old_leader.role = CabalMemberRole.OFFICER.value
        
        # Update the new leader's role
        member.role = CabalMemberRole.LEADER.value
        
        # Update the cabal
        self.leader_id = new_leader_id
        db.session.commit()
        
        return True, "Cabal leadership transferred successfully"
    
    def add_xp(self, amount):
        """Add XP to the cabal and level up if necessary."""
        self.xp += amount
        
        # Check for level up
        while self.xp >= self.get_xp_for_next_level():
            self.level_up()
        
        db.session.commit()
        
        return True, f"Added {amount} XP to the cabal"
    
    def level_up(self):
        """Level up the cabal."""
        self.level += 1
        
        # Add some bonus Chadcoin for leveling up
        bonus = self.level * 100
        self.chadcoin_balance += bonus
        
        return True, f"Cabal leveled up to {self.level}!"
    
    def get_xp_for_next_level(self):
        """Get the XP required for the next level."""
        return 1000 * self.level + 500 * (self.level - 1) ** 2
    
    def add_chadcoin(self, amount):
        """Add Chadcoin to the cabal treasury."""
        self.chadcoin_balance += amount
        db.session.commit()
        
        # Record the transaction
        from app.models.transaction import Transaction
        Transaction.record_chadcoin_transaction(
            user_id=self.leader_id,  # Use leader as the transaction owner
            amount=amount,
            description=f"Added {amount} Chadcoin to {self.name} cabal treasury"
        )
        
        return True, f"Added {amount} Chadcoin to the cabal treasury"
    
    def remove_chadcoin(self, amount):
        """Remove Chadcoin from the cabal treasury."""
        if self.chadcoin_balance < amount:
            return False, "Insufficient Chadcoin in treasury"
        
        self.chadcoin_balance -= amount
        db.session.commit()
        
        # Record the transaction
        from app.models.transaction import Transaction
        Transaction.record_chadcoin_transaction(
            user_id=self.leader_id,  # Use leader as the transaction owner
            amount=-amount,
            description=f"Removed {amount} Chadcoin from {self.name} cabal treasury"
        )
        
        return True, f"Removed {amount} Chadcoin from the cabal treasury"
    
    def get_active_members(self):
        """Get all active members of the cabal."""
        return self.members.filter_by(is_active=True).all()
    
    def get_active_member_count(self):
        """Get the count of active members."""
        return self.members.filter_by(is_active=True).count()
    
    def calculate_total_power(self):
        """Calculate the total power of the cabal based on members' Chads."""
        total_power = 0
        
        for member in self.get_active_members():
            from app.models.user import User
            user = User.query.get(member.user_id)
            if user:
                chad = user.get_active_chad()
                if chad:
                    # Sum up the total stats of each member's active Chad
                    chad_stats = chad.get_total_stats()
                    member_power = sum(chad_stats.values())
                    total_power += member_power
        
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
        return f'<CabalMember {self.user_id} in {self.cabal_id} ({self.role})>'
    
    def add_contribution_points(self, amount):
        """Add contribution points to the member."""
        self.contribution_points += amount
        self.last_active_at = datetime.utcnow()
        db.session.commit()
        
        return True, f"Added {amount} contribution points"
    
    def increment_battles_participated(self):
        """Increment the battles participated counter."""
        self.battles_participated += 1
        self.last_active_at = datetime.utcnow()
        db.session.commit()
        
        return True, "Battles participated incremented"
    
    def update_activity(self):
        """Update the member's last active timestamp."""
        self.last_active_at = datetime.utcnow()
        db.session.commit()
        
        return True, "Activity updated" 