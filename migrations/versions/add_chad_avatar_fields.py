"""Add avatar fields to Chad model

Revision ID: add_chad_avatar_fields
Revises: 2023_11_15_tweet_tracker
Create Date: 2023-08-15 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'add_chad_avatar_fields'
down_revision = '2023_11_15_tweet_tracker'  # Chain from tweet tracker migration
branch_labels = None
depends_on = None


def upgrade():
    # Check if chads table exists and get existing columns
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    if 'chads' in inspector.get_table_names():
        chad_columns = [col['name'] for col in inspector.get_columns('chads')]
        
        # Add avatar fields to the chads table if they don't exist
        if 'avatar_path' not in chad_columns:
            op.add_column('chads', sa.Column('avatar_path', sa.String(255), nullable=True))
        if 'avatar_locked' not in chad_columns:
            op.add_column('chads', sa.Column('avatar_locked', sa.Boolean(), default=False))
        if 'avatar_generation_count' not in chad_columns:
            op.add_column('chads', sa.Column('avatar_generation_count', sa.Integer(), default=0))
        if 'avatar_last_generated' not in chad_columns:
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
    # Check if chads table exists and get existing columns
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    if 'chads' in inspector.get_table_names():
        chad_columns = [col['name'] for col in inspector.get_columns('chads')]
        
        # Remove avatar fields from the chads table if they exist
        if 'avatar_last_generated' in chad_columns:
            op.drop_column('chads', 'avatar_last_generated')
        if 'avatar_generation_count' in chad_columns:
            op.drop_column('chads', 'avatar_generation_count')
        if 'avatar_locked' in chad_columns:
            op.drop_column('chads', 'avatar_locked')
        if 'avatar_path' in chad_columns:
            op.drop_column('chads', 'avatar_path') 