"""Add tweet_tracker table

Revision ID: 2023_11_15_tweet_tracker
Revises: 2023_12_15_nft_update
Create Date: 2023-11-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '2023_11_15_tweet_tracker'
down_revision = '2023_12_15_nft_update'  # Chain from NFT model update
branch_labels = None
depends_on = None

def upgrade():
    """Create tweet_tracker table."""
    op.create_table(
        'tweet_tracker',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tweet_id', sa.String(length=50), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.UniqueConstraint('tweet_id')
    )

def downgrade():
    """Remove tweet_tracker table."""
    op.drop_table('tweet_tracker') 