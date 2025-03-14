"""merge multiple migration heads

Revision ID: f78da657fc97
Revises: add_chad_avatar_fields, 2023_11_15_tweet_tracker, e1f4d9c1a346
Create Date: 2025-03-14 17:31:01.692080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f78da657fc97'
down_revision = ('add_chad_avatar_fields', '2023_11_15_tweet_tracker', 'e1f4d9c1a346')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
