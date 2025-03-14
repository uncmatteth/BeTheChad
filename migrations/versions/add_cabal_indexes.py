"""Add indexes to cabal-related tables

Revision ID: b7c2d5ae8f99
Revises: a5b9cd271e41
Create Date: 2023-03-12 10:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'b7c2d5ae8f99'
down_revision = 'a5b9cd271e41'
branch_labels = None
depends_on = None


def upgrade():
    """Add optimizing indexes."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Create cabal_battles table if it doesn't exist
    if 'cabal_battles' not in inspector.get_table_names():
        op.create_table(
            'cabal_battles',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('cabal_id_1', sa.String(36), sa.ForeignKey('cabals.id'), nullable=False),
            sa.Column('cabal_id_2', sa.String(36), sa.ForeignKey('cabals.id'), nullable=False),
            sa.Column('scheduled_at', sa.DateTime, nullable=False),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp())
        )

    # Create cabal_members table if it doesn't exist
    if 'cabal_members' not in inspector.get_table_names():
        op.create_table(
            'cabal_members',
            sa.Column('id', sa.String(36), primary_key=True),
            sa.Column('cabal_id', sa.String(36), sa.ForeignKey('cabals.id'), nullable=False),
            sa.Column('chad_id', sa.String(36), sa.ForeignKey('chads.id'), nullable=False),
            sa.Column('is_active', sa.Boolean, nullable=False, server_default='1'),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp())
        )

    # Add indexes if tables exist and indexes don't
    if 'cabals' in inspector.get_table_names():
        cabal_indexes = [idx['name'] for idx in inspector.get_indexes('cabals')]
        
        # Add index to total_power for leaderboard queries
        if 'ix_cabals_total_power' not in cabal_indexes:
            op.create_index(
                'ix_cabals_total_power',
                'cabals', ['total_power'],
                unique=False
            )
        
        # Add index to is_active for filtering active cabals
        if 'ix_cabals_is_active' not in cabal_indexes:
            op.create_index(
                'ix_cabals_is_active',
                'cabals', ['is_active'],
                unique=False
            )
    
    # Add index to scheduled_at for finding upcoming battles
    if 'cabal_battles' in inspector.get_table_names():
        battle_indexes = [idx['name'] for idx in inspector.get_indexes('cabal_battles')]
        if 'ix_cabal_battles_scheduled_at' not in battle_indexes:
            op.create_index(
                'ix_cabal_battles_scheduled_at',
                'cabal_battles', ['scheduled_at'],
                unique=False
            )
    
    # Add index to cabal_id and is_active for member queries
    if 'cabal_members' in inspector.get_table_names():
        member_indexes = [idx['name'] for idx in inspector.get_indexes('cabal_members')]
        if 'ix_cabal_members_cabal_is_active' not in member_indexes:
            op.create_index(
                'ix_cabal_members_cabal_is_active',
                'cabal_members', ['cabal_id', 'is_active'],
                unique=False
            )
    
    # Add index to created_at for sorting referrals chronologically
    if 'referrals' in inspector.get_table_names():
        referral_indexes = [idx['name'] for idx in inspector.get_indexes('referrals')]
        if 'ix_referrals_created_at' not in referral_indexes:
            op.create_index(
                'ix_referrals_created_at',
                'referrals', ['created_at'],
                unique=False
            )


def downgrade():
    """Remove added indexes and tables."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Drop indexes if they exist
    for table, indexes in [
        ('referrals', ['ix_referrals_created_at']),
        ('cabal_members', ['ix_cabal_members_cabal_is_active']),
        ('cabal_battles', ['ix_cabal_battles_scheduled_at']),
        ('cabals', ['ix_cabals_is_active', 'ix_cabals_total_power'])
    ]:
        if table in inspector.get_table_names():
            table_indexes = [idx['name'] for idx in inspector.get_indexes(table)]
            for index_name in indexes:
                if index_name in table_indexes:
                    op.drop_index(index_name, table_name=table)

    # Drop tables in reverse order
    for table in ['cabal_members', 'cabal_battles']:
        if table in inspector.get_table_names():
            op.drop_table(table) 