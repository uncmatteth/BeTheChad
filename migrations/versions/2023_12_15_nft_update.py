"""NFT model update

Revision ID: 2023_12_15_nft_update
Revises: e1f4d9c1a346
Create Date: 2023-12-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2023_12_15_nft_update'
down_revision = 'e1f4d9c1a346'  # Chain from remove marketplace migration
branch_labels = None
depends_on = None

# ... existing code ... 