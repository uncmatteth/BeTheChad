"""Remove marketplace and add wallet_type

Revision ID: e1f4d9c1a346
Revises: d9f4e8b0e235
Create Date: 2023-03-14 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'e1f4d9c1a346'
down_revision = 'd9f4e8b0e235'
branch_labels = None
depends_on = None


def upgrade():
    """Apply migration upgrades."""
    # Add wallet_type column to users table if it doesn't exist
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    users_columns = [col['name'] for col in inspector.get_columns('users')]
    if 'wallet_type' not in users_columns:
        op.add_column('users', sa.Column('wallet_type', sa.String(20), nullable=True))
    
    # Check if NFTs table exists
    if 'nfts' in inspector.get_table_names():
        # Get existing columns
        nft_columns = [col['name'] for col in inspector.get_columns('nfts')]
        
        # Remove marketplace-related fields from NFTs table if they exist
        if 'is_listed' in nft_columns:
            op.drop_column('nfts', 'is_listed')
        if 'current_price' in nft_columns:
            op.drop_column('nfts', 'current_price')
        if 'listed_at' in nft_columns:
            op.drop_column('nfts', 'listed_at')
        
        # Check if index exists before trying to drop it
        nft_indexes = inspector.get_indexes('nfts')
        if any(idx['name'] == 'ix_nfts_is_listed' for idx in nft_indexes):
            with op.batch_alter_table('nfts', schema=None) as batch_op:
                batch_op.drop_index('ix_nfts_is_listed')


def downgrade():
    """Revert migration changes."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    # Check if NFTs table exists before adding columns back
    if 'nfts' in inspector.get_table_names():
        # Get existing columns
        nft_columns = [col['name'] for col in inspector.get_columns('nfts')]
        
        # Add back marketplace-related fields to NFTs table if they don't exist
        if 'is_listed' not in nft_columns:
            op.add_column('nfts', sa.Column('is_listed', sa.Boolean(), nullable=False, server_default='0'))
        if 'current_price' not in nft_columns:
            op.add_column('nfts', sa.Column('current_price', sa.Integer(), nullable=True))
        if 'listed_at' not in nft_columns:
            op.add_column('nfts', sa.Column('listed_at', sa.DateTime(), nullable=True))
        
        # Check if index exists before trying to create it
        nft_indexes = inspector.get_indexes('nfts')
        if not any(idx['name'] == 'ix_nfts_is_listed' for idx in nft_indexes):
            with op.batch_alter_table('nfts', schema=None) as batch_op:
                batch_op.create_index('ix_nfts_is_listed', ['is_listed'], unique=False)
    
    # Check if users table and wallet_type column exist before dropping
    if 'users' in inspector.get_table_names():
        users_columns = [col['name'] for col in inspector.get_columns('users')]
        if 'wallet_type' in users_columns:
            op.drop_column('users', 'wallet_type') 