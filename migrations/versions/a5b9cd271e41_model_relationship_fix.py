"""Model relationship fixes

Revision ID: a5b9cd271e41
Revises: add_chad_avatar_fields
Create Date: 2023-03-12 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a5b9cd271e41'
down_revision = 'add_chad_avatar_fields'  # Chain from add_chad_avatar_fields
branch_labels = None
depends_on = None

# ... existing code ... 