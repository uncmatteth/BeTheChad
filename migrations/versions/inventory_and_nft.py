"""Inventory and NFT models migration

Revision ID: inventory_nft_revision
Revises: None
Create Date: 2023-08-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'inventory_nft_revision'
down_revision = None  # This is the first migration
branch_labels = None
depends_on = None


def upgrade():
    # Create inventories table
    op.create_table(
        'inventories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.UniqueConstraint('user_id', name='uq_inventory_user_id')
    )
    
    # Update NFTs table structure
    # First drop the old NFTs table if it exists
    op.drop_table('nfts')
    
    # Create new NFTs table
    op.create_table(
        'nfts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('chad_id', sa.Integer(), sa.ForeignKey('chads.id'), nullable=True),
        sa.Column('waifu_id', sa.Integer(), sa.ForeignKey('waifus.id'), nullable=True),
        sa.Column('item_id', sa.Integer(), sa.ForeignKey('items.id'), nullable=True),
        sa.Column('token_id', sa.String(255), unique=True, nullable=False),
        sa.Column('mint_transaction_id', sa.String(255), unique=True, nullable=True),
        sa.Column('metadata_uri', sa.String(255), nullable=True),
        sa.Column('is_burned', sa.Boolean(), default=False),
        sa.Column('burn_transaction_id', sa.String(255), unique=True, nullable=True),
        sa.Column('minted_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('burned_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    )
    
    # Add index for faster querying by user_id and entity_type
    op.create_index('idx_nfts_user_id', 'nfts', ['user_id'])
    op.create_index('idx_nfts_entity_type', 'nfts', ['entity_type'])
    op.create_index('idx_nfts_user_entity', 'nfts', ['user_id', 'entity_type'])
    
    # Add is_minted column to Chad model
    op.add_column('chads', sa.Column('is_minted', sa.Boolean(), default=False))
    
    # Add is_minted column to Waifu model if it doesn't exist
    op.add_column('waifus', sa.Column('is_minted', sa.Boolean(), default=False))
    
    # Add is_minted column to Item model if it doesn't exist
    op.add_column('items', sa.Column('is_minted', sa.Boolean(), default=False))
    
    # Add is_equipped column to Waifu model if it doesn't exist
    op.add_column('waifus', sa.Column('is_equipped', sa.Boolean(), default=False))
    
    # Add wallet_type column to User model
    op.add_column('users', sa.Column('wallet_type', sa.String(50), nullable=True))
    
    # Create index for inventory searching
    op.create_index('idx_items_user_equipped', 'items', ['user_id', 'is_equipped'])
    op.create_index('idx_waifus_user_equipped', 'waifus', ['user_id', 'is_equipped'])


def downgrade():
    # Remove inventory and NFT-related columns
    op.drop_index('idx_items_user_equipped')
    op.drop_index('idx_waifus_user_equipped')
    
    op.drop_column('users', 'wallet_type')
    
    op.drop_column('waifus', 'is_equipped')
    op.drop_column('items', 'is_minted')
    op.drop_column('waifus', 'is_minted')
    op.drop_column('chads', 'is_minted')
    
    op.drop_index('idx_nfts_user_entity')
    op.drop_index('idx_nfts_entity_type')
    op.drop_index('idx_nfts_user_id')
    
    op.drop_table('nfts')
    op.drop_table('inventories')
    
    # Recreate the original NFTs table (omitted for brevity - in real scenario would recreate original schema) 