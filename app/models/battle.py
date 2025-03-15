"""
Battle model for Chad Battles.
"""
from app.extensions import db
from datetime import datetime
import enum
import json
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

class BattleType(enum.Enum):
    """Enum for battle types."""
    PVP = "pvp"
    PVE = "pve"
    TOURNAMENT = "tournament"
    CABAL_WAR = "cabal_war"

class BattleStatus(enum.Enum):
    """Enum for battle statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class BattleAction(enum.Enum):
    """Enum for battle actions."""
    ROAST = "roast"
    FLEX = "flex"
    DEFEND = "defend"
    SPECIAL = "special"

class Battle(db.Model):
    """Battle model for tracking battles between users"""
    __tablename__ = 'battles'
    
    id = Column(Integer, primary_key=True)
    initiator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    winner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # Battle details
    battle_type = Column(String(50), nullable=False, default='standard')
    status = Column(String(20), nullable=False, default='pending')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Battle stats
    initiator_power = Column(Float, nullable=False, default=0)
    target_power = Column(Float, nullable=False, default=0)
    initiator_bonus = Column(Float, nullable=False, default=0)
    target_bonus = Column(Float, nullable=False, default=0)
    
    # Battle outcome
    result_description = Column(Text, nullable=True)
    chadcoin_reward = Column(Integer, nullable=False, default=0)
    xp_reward = Column(Integer, nullable=False, default=0)
    
    # Relationships
    initiator = relationship('User', foreign_keys=[initiator_id], backref='initiated_battles')
    target = relationship('User', foreign_keys=[target_id], backref='received_battles')
    winner = relationship('User', foreign_keys=[winner_id], backref='won_battles')
    
    def __repr__(self):
        return f'<Battle {self.id}: {self.initiator_id} vs {self.target_id}>'
    
    def calculate_power(self):
        """Calculate battle power for both participants"""
        # This is a simplified version for deployment
        # In the full version, we would calculate based on equipped items, level, etc.
        self.initiator_power = 100  # Placeholder
        self.target_power = 100  # Placeholder
        return self.initiator_power, self.target_power
    
    def determine_winner(self):
        """Determine the winner of the battle"""
        # This is a simplified version for deployment
        # In the full version, we would use a more complex algorithm
        initiator_total = self.initiator_power + self.initiator_bonus
        target_total = self.target_power + self.target_bonus
        
        if initiator_total > target_total:
            self.winner_id = self.initiator_id
            self.result_description = "Initiator won the battle!"
        elif target_total > initiator_total:
            self.winner_id = self.target_id
            self.result_description = "Target won the battle!"
        else:
            # It's a tie, no winner
            self.result_description = "The battle ended in a tie!"
        
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        return self.winner_id
    
    def calculate_rewards(self):
        """Calculate rewards for the battle"""
        # This is a simplified version for deployment
        # In the full version, we would use a more complex algorithm
        self.chadcoin_reward = 10
        self.xp_reward = 5
        return self.chadcoin_reward, self.xp_reward
    
    def start_battle(self):
        """Start the battle."""
        if self.status != BattleStatus.PENDING.value:
            return False, "Battle is not in pending status"
        
        self.status = BattleStatus.IN_PROGRESS.value
        self.started_at = datetime.utcnow()
        self.current_turn = 1
        self.battle_log = json.dumps([{
            "turn": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "event": "battle_started",
            "description": f"Battle between {self.initiator_chad.name} and {self.opponent_chad.name if self.opponent_chad else 'NPC'} has begun!"
        }])
        db.session.commit()
        
        return True, "Battle started successfully"
    
    def perform_action(self, user_id, action_type, target=None):
        """Perform a battle action."""
        if self.status != BattleStatus.IN_PROGRESS.value:
            return False, "Battle is not in progress"
        
        # Determine if it's this user's turn
        is_initiator_turn = (self.current_turn % 2 == 1)
        if (is_initiator_turn and user_id != self.initiator_id) or (not is_initiator_turn and user_id != self.opponent_id):
            return False, "It's not your turn"
        
        # Get the acting chad
        acting_chad = self.initiator_chad if is_initiator_turn else self.opponent_chad
        target_chad = self.opponent_chad if is_initiator_turn else self.initiator_chad
        
        # Process the action
        result = self._process_action(acting_chad, target_chad, action_type, target)
        
        # Update battle log
        self._add_to_battle_log(acting_chad.id, action_type, result)
        
        # Increment turn counter
        self.current_turn += 1
        self.turn_count += 1
        
        # Check if battle should end
        if self._check_battle_end():
            self._end_battle()
        
        db.session.commit()
        
        return True, result
    
    def _process_action(self, acting_chad, target_chad, action_type, target=None):
        """Process a battle action and return the result."""
        # Implementation would depend on game mechanics
        # This is a simplified version
        
        if action_type == BattleAction.ROAST.value:
            damage = acting_chad.get_total_stats()["roast_level"]
            resistance = target_chad.get_total_stats()["cringe_resistance"]
            net_damage = max(1, damage - resistance // 2)
            
            # Apply damage to target's "health" (could be a temporary battle stat)
            # For simplicity, we'll just record the result
            
            return f"{acting_chad.name} roasted {target_chad.name} for {net_damage} damage!"
            
        elif action_type == BattleAction.FLEX.value:
            flex_power = acting_chad.get_total_stats()["clout"]
            
            # Flexing could increase a temporary battle stat or apply a buff
            
            return f"{acting_chad.name} flexed their clout for {flex_power} power!"
            
        elif action_type == BattleAction.DEFEND.value:
            defense = acting_chad.get_total_stats()["cringe_resistance"]
            
            # Defending could increase resistance for the next turn
            
            return f"{acting_chad.name} prepared to defend with {defense} cringe resistance!"
            
        elif action_type == BattleAction.SPECIAL.value:
            drip = acting_chad.get_total_stats()["drip_factor"]
            
            # Special moves could have unique effects based on the chad's class
            
            return f"{acting_chad.name} used a special move with {drip} drip factor!"
        
        return "Invalid action"
    
    def _add_to_battle_log(self, chad_id, action_type, result):
        """Add an action to the battle log."""
        log = json.loads(self.battle_log) if self.battle_log else []
        
        log.append({
            "turn": self.current_turn,
            "timestamp": datetime.utcnow().isoformat(),
            "chad_id": chad_id,
            "action": action_type,
            "result": result
        })
        
        self.battle_log = json.dumps(log)
    
    def _check_battle_end(self):
        """Check if the battle should end."""
        # In a real implementation, this would check health points or other win conditions
        # For simplicity, we'll end after a certain number of turns
        return self.turn_count >= 10
    
    def _end_battle(self):
        """End the battle and determine the winner."""
        self.status = BattleStatus.COMPLETED.value
        self.completed_at = datetime.utcnow()
        
        # Determine winner (simplified)
        # In a real implementation, this would be based on remaining health or other metrics
        initiator_score = sum(self.initiator_chad.get_total_stats().values())
        opponent_score = sum(self.opponent_chad.get_total_stats().values()) if self.opponent_chad else 0
        
        if initiator_score > opponent_score:
            self.winner_id = self.initiator_id
            self.loser_id = self.opponent_id
            winner_name = self.initiator_chad.name
            loser_name = self.opponent_chad.name if self.opponent_chad else "NPC"
        else:
            self.winner_id = self.opponent_id
            self.loser_id = self.initiator_id
            winner_name = self.opponent_chad.name if self.opponent_chad else "NPC"
            loser_name = self.initiator_chad.name
        
        # Add final event to battle log
        log = json.loads(self.battle_log) if self.battle_log else []
        log.append({
            "turn": self.current_turn,
            "timestamp": datetime.utcnow().isoformat(),
            "event": "battle_ended",
            "description": f"{winner_name} defeated {loser_name}!"
        })
        self.battle_log = json.dumps(log)
        
        # Process rewards
        if self.winner_id:
            from app.models.transaction import Transaction, TransactionType
            
            # Award Chadcoin to winner
            reward_amount = self.wager_amount * 2 if self.wager_amount > 0 else 100
            
            # Record transaction
            Transaction.record_chadcoin_transaction(
                user_id=self.winner_id,
                amount=reward_amount,
                description=f"Battle reward for defeating {loser_name}",
                related_entity=('chad', self.initiator_chad_id if self.winner_id == self.initiator_id else self.opponent_chad_id)
            )
            
            # Update winner's Chadcoin balance
            from app.models.user import User
            winner = User.query.get(self.winner_id)
            if winner:
                winner.add_chadcoin(reward_amount)
    
    @classmethod
    def get_user_battles(cls, user_id, limit=10):
        """Get battles for a user."""
        return cls.query.filter(
            db.or_(
                cls.initiator_id == user_id,
                cls.opponent_id == user_id
            )
        ).order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def get_active_battles(cls, user_id):
        """Get active battles for a user."""
        return cls.query.filter(
            db.or_(
                cls.initiator_id == user_id,
                cls.opponent_id == user_id
            ),
            cls.status.in_([BattleStatus.PENDING.value, BattleStatus.IN_PROGRESS.value])
        ).order_by(cls.created_at.desc()).all() 