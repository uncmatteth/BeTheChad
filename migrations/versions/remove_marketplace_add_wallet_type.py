"""Remove marketplace and add wallet_type

Revision ID: e1f4d9c1a346
Revises: d9f4e8b0e235
Create Date: 2023-03-14 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e1f4d9c1a346'
down_revision = 'd9f4e8b0e235'
branch_labels = None
depends_on = None


def upgrade():
    """Apply migration upgrades."""
    # Add wallet_type column to user table
    op.add_column('user', sa.Column('wallet_type', sa.String(20), nullable=True))
    
    # Remove marketplace-related fields from NFT table
    op.drop_column('nft', 'is_listed')
    op.drop_column('nft', 'current_price')
    op.drop_column('nft', 'listed_at')
    
    # Remove marketplace-related indices
    with op.batch_alter_table('nft', schema=None) as batch_op:
        batch_op.drop_index('ix_nft_is_listed')


def downgrade():
    """Revert migration changes."""
    # Add back marketplace-related fields to NFT table
    op.add_column('nft', sa.Column('is_listed', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('nft', sa.Column('current_price', sa.Integer(), nullable=True))
    op.add_column('nft', sa.Column('listed_at', sa.DateTime(), nullable=True))
    
    # Add back marketplace-related indices
    with op.batch_alter_table('nft', schema=None) as batch_op:
        batch_op.create_index('ix_nft_is_listed', ['is_listed'], unique=False)
    
    # Remove wallet_type column from user table
    op.drop_column('user', 'wallet_type') 