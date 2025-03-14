"""Add missing user fields

Revision ID: add_missing_user_fields
Revises: e1f4d9c1a346
Create Date: 2024-03-14 22:55:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_missing_user_fields'
down_revision = 'e1f4d9c1a346'
branch_labels = None
depends_on = None

def upgrade():
    # Add missing columns to users table
    op.add_column('users', sa.Column('password_hash', sa.String(128)))
    op.add_column('users', sa.Column('display_name', sa.String(64)))
    op.add_column('users', sa.Column('bio', sa.String(500)))
    op.add_column('users', sa.Column('avatar_url', sa.String(255)))
    op.add_column('users', sa.Column('chadcoin_balance', sa.Integer(), server_default='100'))
    op.add_column('users', sa.Column('last_login', sa.DateTime()))
    op.add_column('users', sa.Column('x_id', sa.String(64), unique=True, nullable=True))
    op.add_column('users', sa.Column('x_username', sa.String(64), unique=True, nullable=True))
    op.add_column('users', sa.Column('x_displayname', sa.String(64), nullable=True))
    op.add_column('users', sa.Column('x_profile_image', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), server_default='0'))

    # Create indexes for efficient queries
    op.create_index('idx_user_username', 'users', ['username'])
    op.create_index('idx_user_email', 'users', ['email'])
    op.create_index('idx_user_x_id', 'users', ['x_id'])
    op.create_index('idx_user_wallet', 'users', ['wallet_address'])
    op.create_index('idx_user_created_at', 'users', ['created_at'])

def downgrade():
    # Drop indexes
    op.drop_index('idx_user_created_at')
    op.drop_index('idx_user_wallet')
    op.drop_index('idx_user_x_id')
    op.drop_index('idx_user_email')
    op.drop_index('idx_user_username')

    # Drop columns
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'x_profile_image')
    op.drop_column('users', 'x_displayname')
    op.drop_column('users', 'x_username')
    op.drop_column('users', 'x_id')
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'chadcoin_balance')
    op.drop_column('users', 'avatar_url')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'display_name')
    op.drop_column('users', 'password_hash') 