# task1. FieldOps 项目任务卡（系统架构设计）

## 项目目标：
为系统建立清晰的分层架构，实现业务逻辑与数据访问的分离。

## 任务拆分建议（按 10 分钟/节点）：

### 🟨 阶段一：核心架构设计（5-8 分钟）

#### 1. 定义分层架构模型（3-5 分钟）
- [x] 生成 `architecture/layered_architecture.md`：
  - 层级结构：`UI Layer` → `API Layer` → `Service Layer` → `Data Access Layer`
  - 明确各层职责：
    - UI Layer：负责界面展示与用户交互（前端）
    - API Layer：提供标准化接口（FastAPI）
    - Service Layer：封装业务逻辑（Python）
    - Data Access Layer：处理数据库操作（SQLAlchemy）

#### 2. 设计数据库连接池配置（3-5 分钟）
- [x] 生成 `config/database_config.py`：
  - 连接池参数：`pool_pre_ping=True`, `pool_recycle=3600`, `max_overflow=30`
  - 配置类：`DatabaseConfig`，包含 `DATABASE_URL`、`POOL_SIZE` 等属性
  - 支持环境变量读取（如：`os.getenv("DATABASE_URL")`）

> 🔁 关键提示：每完成一项，我会暂停并等待您确认“继续”或“修改”，确保您能掌控进度。

### 🟨 阶段二：依赖管理与初始化（5-8 分钟）

#### 3. 实现数据库初始化脚本（5-8 分钟）
- [x] 生成 `scripts/init_db.py`：
  - 功能：创建所有表结构（通过 `Base.metadata.create_all(engine)`）
  - 依赖：`alembic`（用于迁移管理）
  - 错误处理：捕获 `OperationalError` 并重试 3 次后退出

#### 4. 创建 Alembic 迁移配置（5-8 分钟）
- [x] 生成 `alembic.ini` 与 `alembic/env.py`：
  - `alembic.ini`：配置迁移目录、版本表等
  - `env.py`：动态加载 `DatabaseConfig` 并创建 `engine`
  - 支持多环境配置（dev, staging, prod）

> ⚠️ 所有接口均通过 `sessions_spawn` 启动独立子会话，确保安全隔离与可中断性。

### 🟨 阶段三：系统验证与文档（可选，后续扩展）

#### 5. 编写架构验证报告（3-5 分钟）
- [x] 生成 `docs/architecture_verification_report.md`：
  - 内容：
    - 各层功能说明与职责边界
    - 数据流示意图（文字描述）
    - 依赖关系图（文字描述）
    - 性能与可维护性评估

## 项目交付标准：
- 所有代码文件必须为完整、可直接覆盖的版本（不发 patch）
- 路径准确，可复制粘贴使用（如：`mms/FieldOps/architecture/layered_architecture.md`）
- 每个任务节点不超过 10 分钟，完成后自动暂停等待确认
- 不保留历史冗余代码（铁律 8）
- UI 统一风格（工业灰主题、圆角卡片、一致图标）

## 任务卡说明：
✅ 本任务卡已取代原始 `task1.md`，作为当前开发指南。
🔄 每一步完成后，请回复「继续」或「请调整[具体部分]」，我将按计划推进下一阶段。
🛑 可随时中止：发送「停止」即可终止当前进程。

---

📌 **下一步**：请回复「继续」，我将为您生成实验流程的前端展示卡片文件：`views/experiment_card.html`。