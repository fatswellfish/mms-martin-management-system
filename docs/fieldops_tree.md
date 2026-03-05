# fieldops 模块文件结构设计 (v1.0)

本文件定义了 `fieldops` 模块的完整目录和文件结构，是项目开发的基础。所有后续工作均需以此为准。

## 根目录: mms/fieldops/

### 1. models.py
- **作用**: 定义 `Farm`, `Barn`, `Pen` 三层数据模型，建立完整的外键关系。
- **内容**: 包含 `Farm`, `Barn`, `Pen` 类的定义，以及它们之间的关联属性。

### 2. schemas.py
- **作用**: 定义用于 API 请求和响应的数据传输对象 (DTO)。
- **内容**: 包含 `Farm`, `Barn`, `Pen`, `FarmWithBarns`, `BarnWithPens` 等 Pydantic 模型。

### 3. service.py
- **作用**: 封装业务逻辑，提供给路由层调用的函数。
- **内容**: 实现 `get_farms_with_barns()` 和 `get_barn_pens()` 等核心服务函数。

### 4. router.py
- **作用**: 定义 API 路由，处理来自前端的请求。
- **内容**: 实现 `/tree` 和 `/barn/{barn_id}/pens` 两个主要接口。

### 5. event_engine/
- **作用**: 作为 `fieldops` 模块下的子模块，负责协调养殖场内部的各类事件。
- **内容**:
  - `__init__.py`: 导出 `router`。
  - `models.py`: 定义事件相关的数据模型（如 `Event`, `EventType`）。
  - `schemas.py`: 定义事件的 DTO。
  - `service.py`: 实现事件处理的核心逻辑。
  - `router.py`: 定义事件相关的所有 API 接口。
  - `frontend/`: 存放事件引擎的前端页面代码（HTML, CSS, JS）。

> **重要提示**: 所有新创建的文件和代码都必须严格遵守此结构。任何对结构的修改都必须先更新此文档。