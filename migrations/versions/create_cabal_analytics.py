"""Create cabal analytics table

Revision ID: c8f3e7a9d124
Revises: b7c2d5ae8f99
Create Date: 2023-03-12 10:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c8f3e7a9d124'
down_revision = 'b7c2d5ae8f99'
branch_labels = None
depends_on = None


def upgrade():
    """Create cabal_analytics table."""
    op.create_table(
        'cabal_analytics',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('cabal_id', sa.String(36), sa.ForeignKey('cabal.id'), nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False, default=sa.func.now()),
        sa.Column('member_count', sa.Integer, nullable=False),
        sa.Column('active_member_count', sa.Integer, nullable=False),
        sa.Column('total_power', sa.Float, nullable=False),
        sa.Column('rank', sa.Integer, nullable=False),
        sa.Column('battles_won', sa.Integer, nullable=False),
        sa.Column('battles_lost', sa.Integer, nullable=False),
        sa.Column('referrals', sa.Integer, nullable=False)
    )
    
    # Create index on cabal_id and timestamp for efficient querying
    op.create_index(
        op.f('ix_cabal_analytics_cabal_id_timestamp'),
        'cabal_analytics', ['cabal_id', 'timestamp'],
        unique=False
    )


def downgrade():
    """Drop cabal_analytics table."""
    op.drop_index(op.f('ix_cabal_analytics_cabal_id_timestamp'), table_name='cabal_analytics')
    op.drop_table('cabal_analytics') 