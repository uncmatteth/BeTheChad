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
down_revision = 'inventory_nft_revision'  # Chain from the inventory_nft_revision
branch_labels = None
depends_on = None


def upgrade():
    # Drop existing constraints and indices
    op.drop_constraint('nfts_token_id_key', 'nfts', type_='unique')
    op.drop_constraint('nfts_mint_transaction_id_key', 'nfts', type_='unique', if_exists=True)
    op.drop_constraint('nfts_burn_transaction_id_key', 'nfts', type_='unique', if_exists=True)
    
    # Drop foreign keys
    op.drop_constraint('nfts_user_id_fkey', 'nfts', type_='foreignkey')
    op.drop_constraint('nfts_chad_id_fkey', 'nfts', type_='foreignkey', if_exists=True)
    op.drop_constraint('nfts_waifu_id_fkey', 'nfts', type_='foreignkey', if_exists=True)
    op.drop_constraint('nfts_item_id_fkey', 'nfts', type_='foreignkey', if_exists=True)
    
    # Rename user_id to owner_id
    op.alter_column('nfts', 'user_id', new_column_name='owner_id')
    
    # Add entity_id column
    op.add_column('nfts', sa.Column('entity_id', sa.Integer(), nullable=True))
    
    # Update entity_id based on existing data
    op.execute("""
    UPDATE nfts 
    SET entity_id = CASE 
        WHEN entity_type = 'chad' THEN chad_id 
        WHEN entity_type = 'waifu' THEN waifu_id 
        WHEN entity_type = 'item' THEN item_id 
    END
    """)
    
    # Make entity_id not nullable
    op.alter_column('nfts', 'entity_id', nullable=False)
    
    # Rename mint_transaction_id to transaction_id
    op.alter_column('nfts', 'mint_transaction_id', new_column_name='transaction_id', nullable=True)
    
    # Make transaction_id not nullable with a default value for existing records
    op.execute("UPDATE nfts SET transaction_id = 'legacy_' || id::text WHERE transaction_id IS NULL")
    op.alter_column('nfts', 'transaction_id', nullable=False)
    
    # Make metadata_uri not nullable with a default value for existing records
    op.execute("UPDATE nfts SET metadata_uri = 'https://chadbattles.com/static/metadata/legacy_' || id::text || '.json' WHERE metadata_uri IS NULL")
    op.alter_column('nfts', 'metadata_uri', nullable=False)
    
    # Drop columns we no longer need
    op.drop_column('nfts', 'chad_id')
    op.drop_column('nfts', 'waifu_id')
    op.drop_column('nfts', 'item_id')
    op.drop_column('nfts', 'is_burned')
    op.drop_column('nfts', 'burn_transaction_id')
    op.drop_column('nfts', 'burned_at')
    op.drop_column('nfts', 'minted_at')
    
    # Add unique constraint on token_id
    op.create_unique_constraint('nfts_token_id_key', 'nfts', ['token_id'])
    
    # Add foreign key for owner_id
    op.create_foreign_key('nfts_owner_id_fkey', 'nfts', 'users', ['owner_id'], ['id'])
    
    # Add index on entity_type and entity_id
    op.create_index('ix_nfts_entity_type_entity_id', 'nfts', ['entity_type', 'entity_id'], unique=True)


def downgrade():
    # Drop new constraints and indices
    op.drop_index('ix_nfts_entity_type_entity_id', 'nfts')
    op.drop_constraint('nfts_owner_id_fkey', 'nfts', type_='foreignkey')
    op.drop_constraint('nfts_token_id_key', 'nfts', type_='unique')
    
    # Add back the old columns
    op.add_column('nfts', sa.Column('minted_at', sa.DateTime(), nullable=True))
    op.add_column('nfts', sa.Column('burned_at', sa.DateTime(), nullable=True))
    op.add_column('nfts', sa.Column('burn_transaction_id', sa.String(length=255), nullable=True))
    op.add_column('nfts', sa.Column('is_burned', sa.Boolean(), nullable=True))
    op.add_column('nfts', sa.Column('chad_id', sa.Integer(), nullable=True))
    op.add_column('nfts', sa.Column('waifu_id', sa.Integer(), nullable=True))
    op.add_column('nfts', sa.Column('item_id', sa.Integer(), nullable=True))
    
    # Rename transaction_id back to mint_transaction_id
    op.alter_column('nfts', 'transaction_id', new_column_name='mint_transaction_id', nullable=True)
    
    # Update the entity-specific ID columns based on entity_type and entity_id
    op.execute("""
    UPDATE nfts 
    SET chad_id = CASE WHEN entity_type = 'chad' THEN entity_id ELSE NULL END,
        waifu_id = CASE WHEN entity_type = 'waifu' THEN entity_id ELSE NULL END,
        item_id = CASE WHEN entity_type = 'item' THEN entity_id ELSE NULL END,
        is_burned = FALSE,
        minted_at = created_at
    """)
    
    # Drop the entity_id column
    op.drop_column('nfts', 'entity_id')
    
    # Rename owner_id back to user_id
    op.alter_column('nfts', 'owner_id', new_column_name='user_id')
    
    # Add back the old constraints
    op.create_foreign_key('nfts_user_id_fkey', 'nfts', 'users', ['user_id'], ['id'])
    op.create_foreign_key('nfts_chad_id_fkey', 'nfts', 'chads', ['chad_id'], ['id'])
    op.create_foreign_key('nfts_waifu_id_fkey', 'nfts', 'waifus', ['waifu_id'], ['id'])
    op.create_foreign_key('nfts_item_id_fkey', 'nfts', 'items', ['item_id'], ['id'])
    op.create_unique_constraint('nfts_mint_transaction_id_key', 'nfts', ['mint_transaction_id'])
    op.create_unique_constraint('nfts_burn_transaction_id_key', 'nfts', ['burn_transaction_id'])
    op.create_unique_constraint('nfts_token_id_key', 'nfts', ['token_id']) 