# MMS 项目文件结构设计 (v1.0)

本文件定义了整个 `mms` 项目的完整目录和文件结构，是项目开发的基础。所有后续工作均需以此为准。

## 根目录: mms/

### 1. system_core/
- **作用**: 提供系统基础功能和通用服务，是整个系统的基石。
- **内容**:
  - `models.py`: 定义所有模块共享的数据模型（如用户、权限）
  - `schemas.py`: 定义数据传输对象（DTO），用于API请求/响应格式化。
  - `repository.py`: 提供通用的数据访问层接口，支持多种数据库。
  - `service.py`: 封装业务逻辑，是各模块调用的核心服务。
  - `router.py`: 提供全局路由，管理 `/system-core` 前缀下的所有端点。

### 2. q1_organization_and_planning/
- **作用**: 管理组织结构和资源规划，符合 ISO9001 标准第5章要求。
- **内容**:
  - `__init__.py`
  - `models.py`
  - `schemas.py`
  - `service.py`
  - `router.py`

### 3. q2_support_processes/
- **作用**: 处理日常运营中的支持性任务，符合 ISO9001 标准第6章要求。
- **内容**:
  - `__init__.py`
  - `models.py`
  - `schemas.py`
  - `service.py`
  - `router.py`

### 4. q3_operational_processes/
- **作用**: 管理核心生产活动，符合 ISO9001 标准第7章要求。
- **内容**:
  - `__init__.py`
  - `models.py`
  - `schemas.py`
  - `service.py`
  - `router.py`

### 5. q4_performance_and_improvement/
- **作用**: 分析数据，驱动持续优化，符合 ISO9001 标准第9章要求。
- **内容**:
  - `__init__.py`
  - `models.py`
  - `schemas.py`
  - `service.py`
  - `router.py`

### 6. fieldops/
- **作用**: 管理农场的物理结构和生产批次的逻辑关系，是系统的核心数据源之一。
- **内容**:
  - `models.py`: 定义 `Farm`, `Barn`, `Pen` 三层数据模型。
  - `schemas.py`: 定义数据序列化方案。
  - `service.py`: 封装业务逻辑。
  - `router.py`: 定义核心 API 路由。
  - `event_engine/`: 作为 `fieldops` 模块下的子模块，负责协调养殖场内部的各类事件。
    - `__init__.py`: 导出 `router`。
    - `models.py`: 定义事件相关的数据模型（如 `Event`, `EventType`）。
    - `schemas.py`: 定义事件的 DTO。
    - `service.py`: 实现事件处理的核心逻辑。
    - `router.py`: 定义事件相关的所有 API 接口。
  - `index.html`: **fieldops 模块的主页，非 `event_engine` 的主页。**
    > **重要提示**: 所有新创建的文件和代码都必须严格遵守此结构。任何对结构的修改都必须先更新此文档。