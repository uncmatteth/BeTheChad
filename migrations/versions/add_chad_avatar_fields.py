"""Add avatar fields to Chad model

Revision ID: add_chad_avatar_fields
Revises: inventory_nft_revision
Create Date: 2023-08-15 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_chad_avatar_fields'
down_revision = 'inventory_nft_revision'  # Make sure to chain from the previous revision
branch_labels = None
depends_on = None


def upgrade():
    # Add avatar fields to the chads table
    op.add_column('chads', sa.Column('avatar_path', sa.String(255), nullable=True))
    op.add_column('chads', sa.Column('avatar_locked', sa.Boolean(), default=False))
    op.add_column('chads', sa.Column('avatar_generation_count', sa.Integer(), default=0))
    op.add_column('chads', sa.Column('avatar_last_generated', sa.DateTime(), nullable=True))
    
    # Create directories for avatar storage
    import os
    from flask import current_app
    
    # This code will run during migration
    with op.get_context().connection.begin():
        # Create directories for avatar storage if they don't exist
        for directory in ['default', 'generated', 'preview']:
            avatar_dir_path = f"app/static/img/chad/{directory}"
            if not os.path.exists(avatar_dir_path):
                os.makedirs(avatar_dir_path, exist_ok=True)


def downgrade():
    # Remove avatar fields from the chads table
    op.drop_column('chads', 'avatar_last_generated')
    op.drop_column('chads', 'avatar_generation_count')
    op.drop_column('chads', 'avatar_locked')
    op.drop_column('chads', 'avatar_path') 