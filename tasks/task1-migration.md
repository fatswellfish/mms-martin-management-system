# task1-migration.md - 数据迁移与架构演进（已拆分）

## 迁移目标：
将旧系统 `mms_legacy` 中的结构数据迁移到新系统 `mms/FieldOps`，确保数据一致性与可维护性。

## 迁移原则：
- 仅读取 `mms_legacy` 中的模板与模型文件（不修改原系统）
- 所有新代码必须写入 `mms/FieldOps/` 目录
- 不保留历史冗余代码（铁律 8）
- 使用统一路径命名规范（小写+下划线）

## 已完成迁移内容：
- ✅ 所有 HTML 模板已复制至 `mms/FieldOps/views/`
- ✅ 静态资源（CSS/JS）加载正常，路径正确
- ✅ Jinja2 模板加载器已修复，支持 `farm/` 与 `field_ops/` include
- ✅ URL 重写规则生效：`/pig-farm/*` → `/FieldOps/*`

## 待迁移任务：
- 🔧 `models/pig_batch_locations.py` → 新 `models/location.py`（已完成设计）
- 🔧 `models/pig_batches.py` → 新 `models/batch.py`（待实现）
- 🔧 `models/pig_batch_events.py` → 新 `models/event.py`（待实现）
- 🔧 `legacy/app/routers/farm/` → 新 `router.py`（扩展）

## 迁移验证标准：
- 所有新模型必须通过 `SQLAlchemy ORM` 定义，禁止原生 SQL
- 所有外键必须显式声明，避免数据库依赖漏洞
- 必须生成 `Alembic` 迁移脚本，支持未来数据库切换（SQLite → PostgreSQL）

> 📌 当前状态：迁移工作已按模块拆分，当前处于「位置体系模型」开发阶段。