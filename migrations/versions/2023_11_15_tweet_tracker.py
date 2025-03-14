"""Add tweet_tracker table

Revision ID: 2023_11_15_tweet_tracker
Revises: 2023_12_15_nft_update
Create Date: 2023-11-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '2023_11_15_tweet_tracker'
down_revision = '2023_12_15_nft_update'  # Chain from NFT model update
branch_labels = None
depends_on = None 