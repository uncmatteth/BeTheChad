from app.extensions import db
from datetime import datetime

class TweetTracker(db.Model):
    """Model to track tweets posted by the system and manage reply status."""
    
    __tablename__ = 'tweet_tracker'
    
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.String(64), unique=True, nullable=False)
    tweet_type = db.Column(db.String(64), nullable=False)  # e.g., 'stats_update', 'leaderboard', etc.
    replied_to = db.Column(db.Boolean, default=False)  # Whether we've processed replies to this tweet
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TweetTracker {self.id}: {self.tweet_type} {self.tweet_id}>' 