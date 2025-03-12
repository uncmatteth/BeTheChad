"""Create referral model table

Revision ID: d9f4e8b0e235
Revises: c8f3e7a9d124
Create Date: 2023-03-13 09:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = 'd9f4e8b0e235'
down_revision = 'c8f3e7a9d124'
branch_labels = None
depends_on = None


def upgrade():
    """Create referral table."""
    op.create_table(
        'referral',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('referrer_id', sa.String(36), sa.ForeignKey('chad.id'), nullable=False),
        sa.Column('referred_id', sa.String(36), sa.ForeignKey('chad.id'), nullable=False),
        sa.Column('cabal_id', sa.String(36), sa.ForeignKey('cabal.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('bonus_awarded', sa.Boolean, nullable=False, server_default='0'),
        sa.Column('milestone_bonus_awarded', sa.Boolean, nullable=False, server_default='0')
    )
    
    # Create indexes for better query performance
    op.create_index('idx_referral_referrer', 'referral', ['referrer_id'])
    op.create_index('idx_referral_referred', 'referral', ['referred_id'])
    op.create_index('idx_referral_cabal', 'referral', ['cabal_id'])
    op.create_index('idx_referral_created_at', 'referral', ['created_at'])


def downgrade():
    """Drop referral table."""
    op.drop_index('idx_referral_created_at', 'referral')
    op.drop_index('idx_referral_cabal', 'referral')
    op.drop_index('idx_referral_referred', 'referral')
    op.drop_index('idx_referral_referrer', 'referral')
    op.drop_table('referral') 