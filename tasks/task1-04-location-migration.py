# mms/FieldOps/migrations/versions/location_models.py

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

"""
迁移脚本：创建位置体系模型（Farm, Barn, Pen）
路径：mms/FieldOps/migrations/versions/location_models.py
"""

revision = 'a1b2c3d4e5f6'
depends_on = None
branch_labels = None
depends_on = None

def upgrade():
    """
    建立数据库表结构：farm, barn, pen
    - 所有表使用小写+下划线命名规范
    - 外键关联清晰，支持级联删除
    - 添加索引提升查询性能（特别是 barn_type）
    """
    # 1. 创建 Farm 表
    op.create_table(
        'farm',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 2. 创建 Barn 表
    op.create_table(
        'barn',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('farm_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('barn_type', sa.String(length=20), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False, default=30),
        sa.Column('is_reserved', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['farm_id'], ['farm.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 3. 为 barn_type 建立索引（提升按类型筛选性能）
    op.create_index('ix_barn_barn_type', 'barn', ['barn_type'], unique=False)
    
    # 4. 创建 Pen 表
    op.create_table(
        'pen',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('barn_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=20), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False, default=15),
        sa.Column('current_quantity', sa.Integer(), nullable=False, default=0),
        sa.Column('is_reserved', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['barn_id'], ['barn.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 5. 为 pen 表建立复合索引（提升多条件查询效率）
    op.create_index('ix_pen_barn_id', 'pen', ['barn_id'], unique=False)


def downgrade():
    """
    回滚操作：删除所有位置相关表（用于版本回退）
    """
    op.drop_table('pen')
    op.drop_table('barn')
    op.drop_table('farm')