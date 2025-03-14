"""NFT model update

Revision ID: 2023_12_15_nft_update
Revises: inventory_nft_revision
Create Date: 2023-12-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2023_12_15_nft_update'
down_revision = 'inventory_nft_revision'  # Chain from base migration
branch_labels = None
depends_on = None

def upgrade():
    """Apply migration upgrades."""
    # No schema changes needed as this is a documentation migration
    pass

def downgrade():
    """Revert migration changes."""
    # No schema changes to revert
    pass

# ... existing code ... 