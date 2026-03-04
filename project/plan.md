# FieldOps 项目策划与模块拆解规划（基于 ISO9001 框架）

## 一、总体目标（一句话版）
Field Ops 必须成为一个结构统一、数据清晰、UI 一致、可长期维护、可随时升级、可未来联网、可法规切换、可扩展为独立系统的现场管理平台。

## 二、项目定位与愿景（依据 task1）
- **系统定位**：现场管理核心子系统，用于：
  - 现场结构化管理（类型 → 舍 → 栏）
  - 动物批次生命周期管理
  - 事件驱动运行状态
  - 养殖/实验数据采集
  - 可视化栏位矩阵与批次流转图
  - 风险管理与运行监控
- **未来目标**：
  - 可独立部署为单体系统
  - 可与主系统（QMS/ERP）松耦合同步
  - 可演化为联网协同平台（云部署）
  - 具备风险控制与现场监控能力
  - 可与 IoT 设备联动（重量、体温、摄像头等）

## 三、设计标准与法规框架（依据 task1）
- **ISO 9001:2015 母框架**：
  - 4 组织环境 / 5 领导作用 / 6 策划（风险管理） / 7 支持（资源、文件与记录） / 8 运行（过程控制） / 9 绩效评价 / 10 改进（持续改进）
  - 要求：数据完整性、审计可追踪性、记录不可抵赖性、生命周期与变更管理、风险管理驱动体系。
- **未来扩展**：
  - GMP/GLP/ISO13485 视图切换能力，支持字段与流程的动态切换。
  - UI 必须具备“法规模式切换能力”。

## 四、技术架构要求（依据 task1）
- **架构基座**：
  - 可模块化（Modular Architecture）
  - 可替换 UI 模式（多视图制）
  - 可迁移数据库（SQLite → PostgreSQL/MySQL）
  - 可扩展为多用户联网系统
  - 前后端松耦合（当前为 Jinja2+HTMX，未来可剥离前端）
- **数据层**：
  - 必须使用 SQLAlchemy ORM 作为唯一数据访问方式（禁止原生 sqlite.execute）
  - 所有模型必须有类定义（models/）
  - 数据表命名规范，支持迁移，为未来云数据库做好准备。
  - ORM 模型需具备：清晰字段定义、外键关联、关系（relationship）、数据层可扩展。
- **前端层**：
  - 使用 Jinja2 模板管理 UI
  - 使用 HTMX 实现动态刷新与现代体验（不依赖 React/Vue）
  - 所有页面继承 `base_field_ops.html`
  - 组件化：Card、Scroller、Tag、Icon
  - UI 可根据法规模式切换样式（ISO/GMP 切换）

## 五、模块化结构（依据 task1）
Field Ops 必须严格模块化，低耦合、高内聚。核心模块如下：
1. **结构模块**（Category/Barn/Pen）
2. **批次模块**（Batch）
3. **事件系统**（Event Engine）
4. **位置系统**（Location）
5. **追踪系统**（Trace）
6. **可视化系统**（Dashboard）
7. **风险评估模块**（未来）
8. **法规视图切换模块**（未来）

> ✅ **优先级说明**：
> 本次任务中，`fieldops` 是首要模块，需立即启动开发。其余模块按需求逐步实现。

## 六、开发铁律（必须遵守）
- **铁律 0**：你是决策者，我执行。你提出功能，我给完整实现。
- **铁律 1**：只给结果，不给解释。除非你主动要求。
- **铁律 2**：所有代码必须一次性交付“完整文件”，不允许发 patch、修改建议或手工合并。
- **铁律 3**：不重复修改同一段代码，一次性设计、一轮到位。
- **铁律 4**：不猜你的文件内容。你贴出原文件 → 我给完整新文件。
- **铁律 5**：所有路径必须为准确路径（可复制），如：`app/templates/field_ops/pages/dashboard.html`。
- **铁律 6**：你说“继续”，我就执行下一个模块。
- **铁律 7**：你说“不满意”，我立即重做。
- **铁律 8**：禁止多套结构并存，必须统一体系，无历史垃圾。
- **铁律 9**：UI 必须绝对统一（颜色、圆角、图标集、滚动条风格等）。
- **铁律 10**：系统必须为未来可维护性与可扩展性设计（支持云化、多人协作、IoT接入、法规切换等）。

## 七、未来扩展要求（必须提前预留）
- **4.1 法规视图切换（Regulation Switch）**：
  - 支持切换：ISO、GMP、GLP、ISO13485
  - UI 可切换字段可见性，事件字段可按法规模式自动切换。
- **4.2 风险管理模块（Risk Control）**：
  - 支持风险登记、评分模型、关联事件、趋势图、与批次/不符合联动。
- **4.3 数据可视化模块（Dashboard/大屏）**：
  - 支持栏位矩阵（可缩放）、批次颜色标识、死亡热力图、舍级运行状态、批次趋势图、多批次叠加分析。
- **4.4 多用户协同 & 未来云化**：
  - ORM 数据库可切换，API 层已抽象，不依赖强浏览器特性，未来可切换为 SPA 前端（不锁死）。

## 八、项目实施路径（依序推进）
根据 `FIELDOPS_PROJECT_STATUS.md` 中的待办工作，制定以下开发顺序：

### 🚀 第一阶段：基础模块搭建（优先级最高）
1. **生成 `models/` 层**（ORM 模型定义）
   - `models/category.py`（农场类别）
   - `models/barn.py`（猪舍）
   - `models/pen.py`（猪栏）
   - `models/batch.py`（批次）
   - `models/event.py`（事件）
   - `models/experiment.py`（免疫实验）
2. **生成 `schemas/` 层**（数据校验模型）
   - `schemas/batch_schema.py`
   - `schemas/event_schema.py`
   - `schemas/experiment_schema.py`
3. **生成 `services/` 层**（业务逻辑）
   - `services/batch_service.py`
   - `services/event_service.py`
   - `services/experiment_service.py`
4. **生成 `routers/` 层**（API 路由）
   - `routers/api/batch_router.py`
   - `routers/api/event_router.py`
   - `routers/api/experiment_router.py`
   - `routers/api/tree_router.py`
   - `routers/api/barn_router.py`
   - `routers/api/pen_router.py`

### 🔧 第二阶段：功能联调与数据绑定（中等优先级）
1. 将 API 与前端卡片 UI 联动（通过 HTMX）
2. 实现事件滚动流 `EventScroller` API
3. 完成 `FarmCard`, `BarnCard`, `PenCard`, `BatchCard` 的动态数据绑定

### 📊 第三阶段：高级功能与扩展（未来）
1. 实现法规视图切换模块（`regulation_switch.py`）
2. 开发风险管理模块（`risk_control.py`）
3. 构建大屏可视化系统（`dashboard_panel_mode.py`）
4. 实现多用户协同与云化接口（`multiuser_api.py`）

## 九、总结与行动建议
- ✅ 已完成：
  - 三份文档（业务、状态、知识库）已整合并规范化存储于 `tasks/` 目录下。
  - 项目策划与模块拆解规划已生成，符合 ISO9001 框架与开发铁律。
- 🚀 下一步行动：
  - 请下达指令：“开始生成 models/ 层” 或 “继续” 以启动第一阶段开发。
  - 若对规划有任何不满意，可直接说“不满意”，我将立即重做。

> 💡 提示：所有代码将以“完整文件”形式交付，路径精确，可直接覆盖。无需手动合并。