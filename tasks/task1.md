# task1. FieldOps 项目任务卡（精简版）

## 项目目标：
实现一个可独立部署、模块化、符合 ISO9001 标准的现场管理系统（FieldOps），支持养殖场结构管理、批次生命周期、事件驱动运行、数据可视化与未来扩展能力。

## 任务拆分建议（按 10 分钟/节点）：

### 🟩 阶段一：环境准备与基础架构（预计 5-10 分钟）
- [ ] 确认 `mms/FieldOps/` 目录结构完整（已存在）
- [ ] 创建 `models/`, `services/`, `schemas/`, `api/`, `views/` 子目录（如缺失）
- [ ] 初始化 `main.py` 和 `router.py`（已有，验证可用性）
- [ ] 验证 Jinja2 模板加载路径正确（已完成）
- [ ] 验证静态资源（CSS/JS）加载正常（已完成）

> ✅ 当前状态：基础框架已就绪，无需重建。

### 🟨 阶段二：核心模型与数据层构建（每项 8-12 分钟，分步执行）

#### 1. 定义位置体系模型（3-5 分钟）
- 生成 `models/location.py`：
  - `Farm`（养殖场）
  - `Barn`（猪舍，含类型字段）
  - `Pen`（猪栏，含容量、预留状态）
  - 建立外键关联（Farm → Barn → Pen）
  - 所有模型使用 SQLAlchemy ORM

#### 2. 定义批次与事件模型（3-5 分钟）
- 生成 `models/batch.py`：
  - `Batch`（批次，含 batch_id, quantity, status）
  - 关联 `Pen`（多对多关系）
  - 支持跨舍移动（Transfer）
- 生成 `models/event.py`：
  - `Event`（事件类型：转栏、死亡、出栏、防疫、生病、治疗等）
  - 包含时间戳、关联对象（batch_id, pen_id, barn_id）
  - 支持事件滚动展示逻辑

#### 3. 生成服务层接口（3-5 分钟）
- 生成 `services/location_service.py`：
  - `get_farm_tree()`：返回农场结构树（包含所有舍、栏）
  - `get_barn_pens(barn_id)`：获取某舍所有栏位及占用情况
- 生成 `services/batch_service.py`：
  - `get_batch_detail(batch_id)`：返回批次详情（含分布、事件）
  - `distribute_batch(batch_id, distribution_map)`：执行分栏逻辑（支持多舍多栏）

> 🔁 **关键提示**：每完成一项，我会暂停并等待您确认“继续”或“修改”，确保您能掌控进度。

### 🟨 阶段三：后端 API 与前端联动（分步推进）

#### 4. 实现 `/api/tree` 接口（5-8 分钟）
- 路由：`GET /FieldOps/api/tree`
- 返回：完整的农场结构树（带层级、状态、数量）
- 数据格式：JSON，兼容前端卡片渲染

#### 5. 实现 `/api/events` 接口（5-8 分钟）
- 路由：`GET /FieldOps/api/events`
- 返回：最近 50 条事件（按时间倒序）
- 字段：event_type, timestamp, batch_id, pen_id, description
- 支持前端滚动条实时更新（事件流）

#### 6. 实现 `/api/batches` 接口（5-8 分钟）
- 路由：`GET /FieldOps/api/batches`
- 返回：当前所有批次列表（含状态、数量、归属栏）
- 支持筛选（如：待转栏、即将出栏）

> ⚠️ 所有接口均通过 `sessions_spawn` 启动独立子会话，确保安全隔离与可中断性。

### 🟨 阶段四：免疫与实验流程设计（可选，后续扩展）
- 生成 `api/experiment` 接口，支持方案 A/B/C 动态决策逻辑
- 提供参数输入：疫苗总量 → 自动计算可执行方案

## 项目交付标准：
- 所有代码文件必须为完整、可直接覆盖的版本（不发 patch）
- 路径准确，可复制粘贴使用（如：`mms/FieldOps/models/batch.py`）
- 每个任务节点不超过 10 分钟，完成后自动暂停等待确认
- 不保留历史冗余代码（铁律 8）
- UI 统一风格（工业灰主题、圆角卡片、一致图标）

## 任务卡说明：
✅ 本任务卡已取代原始 `task1.md`，作为当前开发指南。
🔄 每一步完成后，请回复「继续」或「请调整[具体部分]」，我将按计划推进下一阶段。
🛑 可随时中止：发送「停止」即可终止当前进程。

---

📌 **下一步**：请回复「继续」，我将为您生成第一个模块：`models/location.py`。