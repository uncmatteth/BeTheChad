# Database Migration Guide

## Best Practices

### Table Naming Conventions
- **Always use plural names** for tables (e.g., `users` instead of `user`, `items` instead of `item`)
- Be consistent with table names across all migrations
- Reference the base migration for correct table names
- When in doubt, check `inventory_and_nft.py` for the canonical table names

### Migration Structure
1. **Existence Checks**
   - Always check if tables/columns exist before creating or modifying them
   - Use `Inspector` from SQLAlchemy for checks:
   ```python
   from sqlalchemy.engine.reflection import Inspector
   inspector = Inspector.from_engine(op.get_bind())
   ```

2. **Dependencies**
   - Ensure migrations are properly chained using `down_revision`
   - Avoid duplicate revision IDs
   - Keep the migration chain linear when possible

3. **Column Defaults**
   - Always set appropriate `server_default` for boolean columns
   - Example: `server_default='0'` for boolean fields

### Common Pitfalls
1. **Table Name Inconsistency**
   - Issue: Using singular names (`user`) when the schema uses plural (`users`)
   - Solution: Always reference existing tables and use plural names

2. **Missing Existence Checks**
   - Issue: Assuming tables/columns don't exist
   - Solution: Add proper checks before modifications:
   ```python
   def upgrade():
       # Check if table exists
       inspector = Inspector.from_engine(op.get_bind())
       if 'table_name' not in inspector.get_table_names():
           # Create table
           op.create_table(...)
   ```

3. **Index Creation**
   - Issue: Creating indexes before columns exist
   - Solution: Always add columns before creating indexes on them

4. **Multiple Head Revisions**
   - Issue: Branching migration chains
   - Solution: Keep migrations linear, ensure proper `down_revision` chaining

### Migration Template
```python
"""Description of changes

Revision ID: unique_id
Revises: previous_revision_id
Create Date: timestamp

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'unique_id'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    """Apply migration upgrades."""
    # Get inspector for existence checks
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    # Check if table exists before creating
    if 'table_name' not in inspector.get_table_names():
        op.create_table(
            'table_name',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('is_active', sa.Boolean(), server_default='0'),
            sa.PrimaryKeyConstraint('id')
        )
    
    # Check if column exists before adding
    columns = [col['name'] for col in inspector.get_columns('table_name')]
    if 'new_column' not in columns:
        op.add_column('table_name', sa.Column('new_column', sa.String(50)))
    
    # Create index after ensuring column exists
    indexes = [idx['name'] for idx in inspector.get_indexes('table_name')]
    if 'ix_table_name_new_column' not in indexes:
        op.create_index('ix_table_name_new_column', 'table_name', ['new_column'])

def downgrade():
    """Revert migration changes."""
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    
    # Remove in reverse order
    if 'table_name' in inspector.get_table_names():
        indexes = [idx['name'] for idx in inspector.get_indexes('table_name')]
        if 'ix_table_name_new_column' in indexes:
            op.drop_index('ix_table_name_new_column')
        
        columns = [col['name'] for col in inspector.get_columns('table_name')]
        if 'new_column' in columns:
            op.drop_column('table_name', 'new_column')
        
        op.drop_table('table_name')
```

## Running Migrations

### Development
```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Review the generated migration file
# Make any necessary adjustments

# Apply the migration
flask db upgrade

# If needed, rollback
flask db downgrade
```

### Production
1. Always test migrations in development first
2. Back up the production database before migrating
3. Run migrations during low-traffic periods
4. Have a rollback plan ready

### Troubleshooting

1. **Multiple Head Revisions**
   ```
   Error: Multiple head revisions are present
   ```
   - Check your migration chain
   - Ensure each migration has the correct `down_revision`
   - Use `flask db heads` to see all current heads
   - Merge heads if necessary with a new migration

2. **Table/Column Already Exists**
   - Add existence checks in your migration
   - Use `Inspector` to check before creating

3. **Missing Table/Column**
   - Ensure migrations are being applied in the correct order
   - Check that all necessary migrations are present
   - Verify the migration chain is complete

## Testing Migrations

1. **Test Environment**
   - Use a separate test database
   - Run migrations on a copy of production data
   - Test both upgrade and downgrade paths

2. **Verification**
   - Check that all tables and columns are created correctly
   - Verify indexes are created
   - Test any new constraints
   - Ensure data integrity is maintained

## Maintenance

1. **Regular Cleanup**
   - Remove duplicate migrations
   - Keep migration history linear when possible
   - Document complex migrations

2. **Version Control**
   - Always commit migration files
   - Include meaningful commit messages
   - Tag important migration versions

3. **Documentation**
   - Update schema documentation after migrations
   - Document any manual steps required
   - Keep track of migration dependencies 