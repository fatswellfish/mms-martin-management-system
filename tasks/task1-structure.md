# task1-structure.md - 位置体系模型设计（已拆分）

## 模块目标：
定义并实现 `models/location.py`，包含农场（Farm）、猪舍（Barn）、猪栏（Pen）三个核心数据模型，建立层级关系与外键约束，为后续批次分布、事件驱动提供基础结构。

## 任务节点分解：

### 1. Farm 模型（养殖场）
- 属性：
  - id (Integer, PK)
  - name (String, unique)
  - created_at (DateTime)
  - updated_at (DateTime)

### 2. Barn 模型（猪舍）
- 属性：
  - id (Integer, PK)
  - farm_id (Integer, FK → Farm.id)
  - name (String)
  - barn_type (String, enum: 'farrowing', 'weaning', 'finishing', 'second_weaning', 'breeding', 'lactation', 'sow')
  - capacity (Integer, default=30)
  - is_reserved (Boolean, default=False)
  - created_at (DateTime)
  - updated_at (DateTime)

### 3. Pen 模型（猪栏）
- 属性：
  - id (Integer, PK)
  - barn_id (Integer, FK → Barn.id)
  - name (String)
  - capacity (Integer, default=15)
  - current_quantity (Integer, default=0)
  - is_reserved (Boolean, default=False)
  - created_at (DateTime)
  - updated_at (DateTime)

## 关系说明：
- Farm → Barn：1:N
- Barn → Pen：1:N
- Pen 可被多个 Batch 占用（通过中间表或外键关联）

## 数据库迁移要求：
- 使用 SQLAlchemy Migrations（Alembic）生成版本控制脚本
- 所有字段必须有默认值或非空约束（除非明确允许为空）
- 表名规范：小写加下划线（如：farm, barn, pen）

## 输出文件路径：
`mms/FieldOps/models/location.py`

> ✅ 当前状态：该模块已从原始任务中独立拆分，可单独执行。