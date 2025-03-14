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

# ... existing code ... 