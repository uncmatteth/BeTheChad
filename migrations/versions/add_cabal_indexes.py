"""Add indexes to cabal-related tables

Revision ID: b7c2d5ae8f99
Revises: a5b9cd271e41
Create Date: 2023-03-12 10:05:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b7c2d5ae8f99'
down_revision = 'a5b9cd271e41'
branch_labels = None
depends_on = None


def upgrade():
    """Add optimizing indexes."""
    # Add index to total_power for leaderboard queries
    op.create_index(
        op.f('ix_cabal_total_power'),
        'cabal', ['total_power'],
        unique=False
    )
    
    # Add index to is_active for filtering active cabals
    op.create_index(
        op.f('ix_cabal_is_active'),
        'cabal', ['is_active'],
        unique=False
    )
    
    # Add index to scheduled_at for finding upcoming battles
    op.create_index(
        op.f('ix_cabal_battle_scheduled_at'),
        'cabal_battle', ['scheduled_at'],
        unique=False
    )
    
    # Add index to cabal_id and is_active for member queries
    op.create_index(
        op.f('ix_cabal_member_cabal_is_active'),
        'cabal_member', ['cabal_id', 'is_active'],
        unique=False
    )
    
    # Add index to created_at for sorting referrals chronologically
    op.create_index(
        op.f('ix_referral_created_at'),
        'referral', ['created_at'],
        unique=False
    )


def downgrade():
    """Remove added indexes."""
    op.drop_index(op.f('ix_referral_created_at'), table_name='referral')
    op.drop_index(op.f('ix_cabal_member_cabal_is_active'), table_name='cabal_member')
    op.drop_index(op.f('ix_cabal_battle_scheduled_at'), table_name='cabal_battle')
    op.drop_index(op.f('ix_cabal_is_active'), table_name='cabal')
    op.drop_index(op.f('ix_cabal_total_power'), table_name='cabal') 