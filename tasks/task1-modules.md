# task1-modules.md - 模块化结构说明（已拆分）

## 项目模块划分（按功能职责）：

### 1. 位置体系模块（Location Module）
- 路径：`mms/FieldOps/models/location.py`
- 功能：定义农场、猪舍、猪栏的层级结构与关系，为批次分布提供基础。
- 子任务：
  - Farm 模型（养殖场）
  - Barn 模型（猪舍）
  - Pen 模型（猪栏）
  - 外键关联与数据迁移脚本生成

### 2. 批次与事件模块（Batch & Event Module）
- 路径：`mms/FieldOps/models/batch.py`, `mms/FieldOps/models/event.py`
- 功能：管理动物批次生命周期与事件流，驱动系统状态变化。
- 子任务：
  - Batch 模型（批次信息、数量、状态）
  - Event 模型（事件类型、时间戳、关联对象）
  - 事件滚动机制设计（用于前端展示）

### 3. 服务层模块（Service Layer）
- 路径：`mms/FieldOps/services/location_service.py`, `mms/FieldOps/services/batch_service.py`
- 功能：封装业务逻辑，提供可调用接口。
- 子任务：
  - `get_farm_tree()`：获取完整农场结构树
  - `get_barn_pens(barn_id)`：获取某舍所有栏位及占用情况
  - `distribute_batch(batch_id, distribution_map)`：执行分栏逻辑（支持多舍多栏）

### 4. API 接口模块（API Module）
- 路径：`mms/FieldOps/router.py`（扩展）
- 功能：暴露后端接口供前端调用。
- 子任务：
  - `/api/tree`：返回农场结构树（JSON）
  - `/api/events`：返回最近事件流（用于滚动条）
  - `/api/batches`：返回批次列表（支持筛选）

### 5. 免疫与实验模块（Experiment Module）
- 路径：`mms/FieldOps/api/experiment.py`（待实现）
- 功能：根据疫苗数量动态决策免疫方案（A/B/C）。
- 子任务：
  - 接收疫苗总量参数 → 返回可执行方案 
  - 支持方案自动切换逻辑（如：3600头份 → 方案B）

> 📌 说明：每个模块独立成文件，任务卡按顺序推进。当前处于「位置体系模块」开发阶段。