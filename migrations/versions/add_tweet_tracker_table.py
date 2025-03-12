"""Add tweet_tracker table

Revision ID: 2023_11_15_tweet_tracker
Revises: <!-- previous migration id -->
Create Date: 2023-11-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '2023_11_15_tweet_tracker'
down_revision = None  # Replace with the ID of the previous migration
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tweet_tracker',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tweet_id', sa.String(length=64), nullable=False),
        sa.Column('tweet_type', sa.String(length=64), nullable=False),
        sa.Column('replied_to', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tweet_id')
    )


def downgrade():
    op.drop_table('tweet_tracker') 