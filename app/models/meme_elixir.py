from app import db
from datetime import datetime, timedelta
import uuid

class ElixirType(db.Model):
    """Types of meme elixirs (power-ups)"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    
    # Duration in hours (0 for one-time use)
    duration = db.Column(db.Integer, default=0)
    
    # Cost in Chadcoin
    price = db.Column(db.Integer, default=100)
    
    # Stat boosts (percentage or flat value)
    clout_boost = db.Column(db.Integer, default=0)
    roast_boost = db.Column(db.Integer, default=0)
    cringe_resistance_boost = db.Column(db.Integer, default=0)
    drip_boost = db.Column(db.Integer, default=0)
    
    # Boost type (percentage or flat)
    is_percentage = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    elixirs = db.relationship('MemeElixir', backref='elixir_type', lazy='dynamic')
    
    def __repr__(self):
        return f'<ElixirType {self.name}>'

class MemeElixir(db.Model):
    """Instance of a meme elixir owned by a player"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    elixir_type_id = db.Column(db.String(36), db.ForeignKey('elixir_type.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    
    # Status
    is_used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MemeElixir {self.elixir_type.name} owned by {self.user.x_username}>'
    
    def activate(self, chad):
        """Activate this elixir on a Chad character"""
        if self.is_used:
            return False, "Elixir has already been used"
        
        if self.user_id != chad.user_id:
            return False, "You don't own this elixir"
        
        # Calculate the bonus values
        if self.elixir_type.is_percentage:
            clout_bonus = int(chad.clout * self.elixir_type.clout_boost / 100)
            roast_bonus = int(chad.roast_level * self.elixir_type.roast_boost / 100)
            cringe_bonus = int(chad.cringe_resistance * self.elixir_type.cringe_resistance_boost / 100)
            drip_bonus = int(chad.drip_factor * self.elixir_type.drip_boost / 100)
        else:
            clout_bonus = self.elixir_type.clout_boost
            roast_bonus = self.elixir_type.roast_boost
            cringe_bonus = self.elixir_type.cringe_resistance_boost
            drip_bonus = self.elixir_type.drip_boost
        
        # Calculate expiration time
        if self.elixir_type.duration > 0:
            expires_at = datetime.utcnow() + timedelta(hours=self.elixir_type.duration)
        else:
            # One-time use for the next battle
            expires_at = datetime.utcnow() + timedelta(hours=1)
        
        # Create the active elixir effect
        from app.models.chad import ActiveElixir
        active_elixir = ActiveElixir(
            chad_id=chad.id,
            elixir_id=self.id,
            activated_at=datetime.utcnow(),
            expires_at=expires_at,
            clout_bonus=clout_bonus,
            roast_bonus=roast_bonus,
            cringe_resistance_bonus=cringe_bonus,
            drip_bonus=drip_bonus
        )
        
        # Mark the elixir as used
        self.is_used = True
        self.used_at = datetime.utcnow()
        
        db.session.add(active_elixir)
        db.session.commit()
        
        return True, "Elixir activated successfully" 