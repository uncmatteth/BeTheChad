"""Inventory and NFT models migration

Revision ID: inventory_nft_revision
Revises: None
Create Date: 2023-08-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'inventory_nft_revision'
down_revision = None  # This is the first migration
branch_labels = None
depends_on = None


def upgrade():
    # Create users table if it doesn't exist
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    if 'users' not in inspector.get_table_names():
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('username', sa.String(50), unique=True, nullable=False),
            sa.Column('email', sa.String(120), unique=True, nullable=False),
            sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
            sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
        )

    # Create chads table if it doesn't exist
    if 'chads' not in inspector.get_table_names():
        op.create_table(
            'chads',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
            sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
        )

    # Create waifus table if it doesn't exist
    if 'waifus' not in inspector.get_table_names():
        op.create_table(
            'waifus',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
            sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
        )

    # Create items table if it doesn't exist
    if 'items' not in inspector.get_table_names():
        op.create_table(
            'items',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
            sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
        )

    # Create inventories table if it doesn't exist
    if 'inventories' not in inspector.get_table_names():
        op.create_table(
            'inventories',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
            sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
            sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
            sa.UniqueConstraint('user_id', name='uq_inventory_user_id')
        )
    
    # Check if NFTs table exists before trying to drop it
    if 'nfts' in inspector.get_table_names():
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
    
    # Add columns to existing tables with checks
    for table, columns in [
        ('chads', [('is_minted', sa.Boolean(), False)]),
        ('waifus', [('is_minted', sa.Boolean(), False), ('is_equipped', sa.Boolean(), False)]),
        ('items', [('is_minted', sa.Boolean(), False), ('is_equipped', sa.Boolean(), False)]),
        ('users', [('wallet_type', sa.String(50), True)])
    ]:
        table_columns = [col['name'] for col in inspector.get_columns(table)]
        for col_name, col_type, nullable in columns:
            if col_name not in table_columns:
                op.add_column(table, sa.Column(col_name, col_type, nullable=nullable, server_default='0' if col_type == sa.Boolean() else None))
    
    # Create index for inventory searching after columns are added
    op.create_index('idx_items_user_equipped', 'items', ['user_id', 'is_equipped'])
    op.create_index('idx_waifus_user_equipped', 'waifus', ['user_id', 'is_equipped'])


def downgrade():
    """Remove all created tables and columns in reverse order."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    # Drop indexes first
    if 'items' in inspector.get_table_names():
        op.drop_index('idx_items_user_equipped')
    if 'waifus' in inspector.get_table_names():
        op.drop_index('idx_waifus_user_equipped')
    
    # Drop columns from existing tables
    for table, columns in [
        ('users', ['wallet_type']),
        ('waifus', ['is_equipped', 'is_minted']),
        ('items', ['is_equipped', 'is_minted']),
        ('chads', ['is_minted'])
    ]:
        if table in inspector.get_table_names():
            table_columns = [col['name'] for col in inspector.get_columns(table)]
            for col_name in columns:
                if col_name in table_columns:
                    op.drop_column(table, col_name)
    
    # Drop NFTs table and its indexes
    if 'nfts' in inspector.get_table_names():
        op.drop_index('idx_nfts_user_entity')
        op.drop_index('idx_nfts_entity_type')
        op.drop_index('idx_nfts_user_id')
        op.drop_table('nfts')
    
    # Drop other tables in reverse order
    for table in ['inventories', 'items', 'waifus', 'chads', 'users']:
        if table in inspector.get_table_names():
            op.drop_table(table) 