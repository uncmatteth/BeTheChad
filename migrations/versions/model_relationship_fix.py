"""Model relationship fixes

Revision ID: a5b9cd271e41
Revises: inventory_nft_revision
Create Date: 2023-03-12 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a5b9cd271e41'
down_revision = 'inventory_nft_revision'  # This migration follows the inventory and NFT migration
branch_labels = None
depends_on = None


def upgrade():
    """Apply migration upgrades."""
    # No schema changes needed as the modifications were only to relationship definitions
    # This migration serves as documentation of the relationship fixes
    pass


def downgrade():
    """Revert migration changes."""
    # No schema changes to revert
    pass 