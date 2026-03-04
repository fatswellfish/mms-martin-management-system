"""
Initial schema
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create farms table
    op.create_table(
        'farms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create barns table
    op.create_table(
        'barns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('farm_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['farm_id'], ['farms.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create pens table
    op.create_table(
        'pens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.Column('reserved', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('barn_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['barn_id'], ['barns.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create batches table
    op.create_table(
        'batches',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.String(length=50), nullable=False, unique=True),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create events table
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('batch_id', sa.String(length=50), nullable=False),
        sa.Column('pen_id', sa.Integer(), nullable=True),
        sa.Column('barn_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.batch_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pen_id'], ['pens.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['barn_id'], ['barns.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create transfers table
    op.create_table(
        'transfers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.String(length=50), nullable=False),
        sa.Column('from_pen_id', sa.Integer(), nullable=False),
        sa.Column('to_pen_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.batch_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['from_pen_id'], ['pens.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['to_pen_id'], ['pens.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create batch_pens association table (many-to-many)
    op.create_table(
        'batch_pens',
        sa.Column('batch_id', sa.String(length=50), nullable=False),
        sa.Column('pen_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['batch_id'], ['batches.batch_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pen_id'], ['pens.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('batch_id', 'pen_id')
    )

def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('batch_pens')
    op.drop_table('transfers')
    op.drop_table('events')
    op.drop_table('batches')
    op.drop_table('pens')
    op.drop_table('barns')
    op.drop_table('farms')