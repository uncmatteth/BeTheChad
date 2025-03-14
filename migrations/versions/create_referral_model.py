"""Create referral model table

Revision ID: d9f4e8b0e235
Revises: c8f3e7a9d124
Create Date: 2023-03-13 09:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'd9f4e8b0e235'
down_revision = 'c8f3e7a9d124'
branch_labels = None
depends_on = None


def upgrade():
    """Create referral table."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Create cabal table if it doesn't exist
    if 'cabals' not in inspector.get_table_names():
        op.create_table(
            'cabals',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()),
            sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())
        )

    # Create referral table if it doesn't exist
    if 'referrals' not in inspector.get_table_names():
        op.create_table(
            'referrals',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('referrer_id', sa.String(36), sa.ForeignKey('chads.id'), nullable=False),
            sa.Column('referred_id', sa.String(36), sa.ForeignKey('chads.id'), nullable=False),
            sa.Column('cabal_id', sa.String(36), sa.ForeignKey('cabals.id'), nullable=False),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()),
            sa.Column('bonus_awarded', sa.Boolean, nullable=False, server_default='0'),
            sa.Column('milestone_bonus_awarded', sa.Boolean, nullable=False, server_default='0')
        )
        
        # Create indexes for better query performance
        op.create_index('idx_referrals_referrer', 'referrals', ['referrer_id'])
        op.create_index('idx_referrals_referred', 'referrals', ['referred_id'])
        op.create_index('idx_referrals_cabal', 'referrals', ['cabal_id'])
        op.create_index('idx_referrals_created_at', 'referrals', ['created_at'])


def downgrade():
    """Drop referral and cabal tables."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Drop referrals table and its indexes if they exist
    if 'referrals' in inspector.get_table_names():
        # Drop indexes first
        for index_name in [
            'idx_referrals_created_at',
            'idx_referrals_cabal',
            'idx_referrals_referred',
            'idx_referrals_referrer'
        ]:
            if any(idx['name'] == index_name for idx in inspector.get_indexes('referrals')):
                op.drop_index(index_name, 'referrals')
        op.drop_table('referrals')

    # Drop cabals table if it exists and no other tables depend on it
    if 'cabals' in inspector.get_table_names():
        op.drop_table('cabals') 