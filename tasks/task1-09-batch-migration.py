# mms/FieldOps/migrations/versions/batch_models.py

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

"""
迁移脚本：创建批次与事件模型（Batch, Event）
路径：mms/FieldOps/migrations/versions/batch_models.py
"""

revision = 'b2c3d4e5f6a7'
depends_on = 'a1b2c3d4e5f6'  # 依赖位置体系模块的迁移
branch_labels = None
depends_on = None

def upgrade():
    """
    建立数据库表结构：batch, event
    - 所有表使用小写+下划线命名规范
    - 外键关联清晰，支持级联删除
    - 添加索引提升查询性能（特别是 batch_id、timestamp）
    """
    # 1. 创建 Batch 表
    op.create_table(
        'batch',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('batch_id', sa.String(length=50), nullable=False, unique=True),
        sa.Column('quantity', sa.Integer(), nullable=False, default=600),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', 'transferred', 'out_of_farm'), 
                  nullable=False, default='pending'),
        sa.Column('source_pen_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['source_pen_id'], ['pen.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 2. 为 batch_id 建立唯一索引（提升查询效率）
    op.create_index('ix_batch_batch_id', 'batch', ['batch_id'], unique=True)
    
    # 3. 创建 Event 表
    op.create_table(
        'event',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('event_type', sa.Enum('transfer', 'death', 'exit', 'vaccination', 'sick', 'treatment', 'feeding', 'cleaning', 'other'), 
                  nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('batch_id', sa.String(length=50), nullable=False),
        sa.Column('pen_id', sa.Integer(), nullable=True),
        sa.Column('barn_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('is_processed', sa.Boolean(), nullable=False, default=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 4. 为 batch_id 建立索引（提升按批次查询性能）
    op.create_index('ix_event_batch_id', 'event', ['batch_id'], unique=False)
    
    # 5. 为 timestamp 建立索引（提升时间范围查询性能）
    op.create_index('ix_event_timestamp', 'event', ['timestamp'], unique=False)


def downgrade():
    """
    回滚操作：删除所有批次与事件相关表（用于版本回退）
    """
    op.drop_table('event')
    op.drop_table('batch')