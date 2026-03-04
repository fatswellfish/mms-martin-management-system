task1. FieldOps 项目任务卡
一. 目前我正在做一个综合管理系统
第一章：系统定位与愿景
1.1 系统定位（Field Ops / 现场管理）
Field Ops 是 MMS 综合管理系统的核心子系统之一，用于：

现场结构化管理（类型 → 舍 → 栏）
动物批次生命周期管理
事件驱动现场运行状态
养殖/实验现场数据采集
可视化栏位矩阵与批次流转图
风险管理与运行监控
未来目标：

可独立部署为单体现场系统
可与主系统（QMS/ERP）松耦合同步
可演化为联网协同平台（云部署）
具备风险控制与现场监控能力
可与 IoT 设备联动（重量、体温、摄像头等）
1.2 总体设计遵循的标准与法规框架
Field Ops 必须遵循：

（1）ISO 9001:2015 母框架
包括但不限于：

4 组织环境
5 领导作用
6 策划（风险管理）
7 支持（资源、文件与记录）
8 运行（过程控制）
9 绩效评价
10 改进（持续改进）
要求：

数据完整性
审计可追踪性
记录不可抵赖性
生命周期与变更管理
风险管理驱动体系
（2）GMP / GLP / ISO13485 相关要求（未来扩展）
系统必须具备切换界面能力，让用户可按不同法规视图查看不同的字段与流程。

例：

GMP/GLP 视图：显示批记录、处方、偏差
ISO 视图：显示过程结构、记录控制
现场视图：显示栏状态、批次流向
UI 必须具备“法规模式切换能力”。

第二章：技术架构总体要求
2.1 架构基座
系统必须满足：

可模块化（Modular Architecture）
可替换 UI 模式（多视图制）
可迁移数据库（SQLite → PostgreSQL/MySQL）
可扩展为多用户联网系统
前后端松耦合（即便当前为 Jinja2+HTMX，也可未来剥离前端）
2.2 数据层要求（必须遵守）
使用 SQLAlchemy ORM 作为唯一数据访问方式
不允许原生 sqlite.execute
所有数据模型必须有类定义（models/）
数据表命名必须规范
数据模型必须支持迁移
必须为未来云数据库做好准备（避免 SQLite 专属写法）
要求 ORM 模型具备：

清晰字段定义
外键关联
关系（relationship）
数据层可扩展
2.3 前端层要求（HTMX + Jinja2）
使用 Jinja2 模板管理 UI
使用 HTMX 实现动态刷新与现代体验
不依赖 React/Vue（除非系统未来拆出去）
所有 Field Ops 页面必须继承统一 UI：
base_field_ops.html
组件化（Card、Scroller、Tag、Icon）
UI 可根据法规模式切换样式（ISO/GMP 切换）
2.4 模块化结构要求
Field Ops 必须严格模块化：

TEXT
结构模块（Category/Barn/Pen）
批次模块（Batch）
事件系统（Event Engine）
位置系统（Location）
追踪系统（Trace）
可视化系统（Dashboard）
风险评估模块（未来）
法规视图切换模块（未来）
模块之间低耦合、高内聚。

第三章：开发铁律（不可违反）
铁律 0：你是决策者，我执行。
你提出功能，我给完整实现。

铁律 1：只给结果，不给解释。
除非你主动要求。

铁律 2：所有代码必须一次性交付“完整文件”。
不允许发 patch
不允许给你修改建议
不允许让你手工合并
所有变更必须以“完整文件”形式给出
你只需复制 → 覆盖，即可运行。

铁律 3：不重复修改同一段代码。
一次性设计、一轮到位，避免补丁式烂尾结构。

铁律 4：不猜你的文件内容。
你贴出原文件 → 我给完整新文件。

铁律 5：所有路径必须为准确路径（可复制）。
示例：

TEXT
app/templates/field_ops/pages/dashboard.html
app/routers/farm/pig_farm_event_move_pen.py
app/services/pig_farm_batch_code.py
绝不允许模糊路径。

铁律 6：你说“继续”，我就执行下一个模块。
铁律 7：你说“不满意”，我立即重做。
铁律 8：禁止多套结构并存。
禁止：

farm_structure_old + farm_structure_new
basic_event_old + unified_event
trace_old + trace_new
Field Ops 必须统一体系，无历史垃圾。

铁律 9：UI 必须绝对统一。
统一：

颜色（工业灰主题）
卡片（圆角 8–12px）
事件色条
图标集
滚动条风格
组件样式
页面布局（A 系列）
铁律 10：系统必须为未来可维护性与可扩展性设计。
包括：

未来联机协作（多人）
未来数据中心化
未来 IoT 设备接入
未来法规视图切换
未来拆分部署
未来风控模块加入
未来全文检索/分析模块加入
第四章：未来扩展要求（必须提前预留）
4.1 法规视图切换（Regulation Switch）
UI 和后端都必须支持未来切换法规模式：

ISO
GMP
GLP
ISO13485
UI 可切换字段可见性。
事件字段可按法规模式自动切换。

4.2 风险管理模块（Risk Control）
未来必须支持：

风险登记
风险评分模型
风险关联事件
风险趋势图
风险与批次生命周期联动
风险与不符合（Deviation）联动
数据结构必须可扩展以支持风险相关字段。

4.3 数据可视化模块（Dashboard/大屏）
Field Ops 必须支持：

栏位矩阵（可缩放）
批次颜色标识
死亡热力图
舍级运行状态
批次趋势图
多批次叠加分析
4.4 多用户协同 & 未来云化
必须确保：

ORM 数据库可切换
API 层已抽象
UI 不依赖强浏览器特性
不使用前端编译框架（降低复杂度）
未来可切换为 SPA 前端（不锁死）
第五章：总体目标（一句话版）
Field Ops 必须成为一个结构统一、数据清晰、UI 一致、可长期维护、可随时升级、可未来联网、可法规切换、可扩展为独立系统的现场管理平台。

任务名称：
实现 ISO9001 驱动的 MMS 系统架构（Architecture → Modules → Migration）

已完成（无需重复）
architecture.md 已完成至第 29 部分
核心体系结构确立：
TEXT
enterprise_management_system/
Q1_organization_and_planning/
Q2_support_processes/
Q3_operational_processes/
Q4_performance_and_improvement/
system_core/
FieldOps/
已建立 ISO9001 → 体系过程 → 业务模块 的三级结构
已确认你的最终方向：
体系驱动架构（ISO 母框架为主树）＋业务模块为子实现（非平铺）＋ domain 独立
FieldOps是其中的一个模块,需要优先把它做出来.系统目前开发了一半,还没有调试.代码有部分损坏和错误需要修正.

业务需求（BUSINESS SPEC）：
（养殖场业务设计 + 你的需求 + 实例配置 + 实验流程）

============================================================
FIELDOPS 现场运维系统（养殖场管理）业务文档
版本：2026-02

一、系统定位
FieldOps 是一个用于养殖场现场运维的业务系统，涵盖：
养殖场结构
进猪批次管理
分栏管理
事件管理
免疫（实验）流程管理
实时监控（卡片 UI）
数据滚动（事件滚动栏）
大屏显示模式

二、核心业务领域模型

位置体系（Location Hierarchy）
Farm（养殖场）
├── Barn（猪舍）
│ 每个舍属于一个类别：产房、保育、育肥、二次育肥、繁育、哺乳、母猪等
└── Pen（猪栏）
每栏有容量（capacity）
每栏可以装某批次的猪
有些栏是预留栏：治疗、疗养、留观

动物模型（以批次为核心）
Batch（猪批次）
batch_id（比如 20260228）
由一次运输进入养殖场
总数量为 N
进场后会分散到不同舍、不同栏

分栏逻辑（Batch Distribution）
例子：
一次进场 500 头猪
分布为：
育肥2舍 → 6栏 → 30头
二保育6舍 → 7栏 → 20头
……

分栏逻辑要求：
允许同一批次拆分到多个舍/多个栏
每栏记录 batch_id + quantity
跨舍移动（transfer event）

事件（Events）
事件是系统核心数据，用于驱动状态和卡片 UI 展示。
事件类型包括：
转栏（Transfer）
出栏（Sale）
防疫（Vaccination）
死亡（Death）
生病（Illness）
治疗（Treatment）
分批出栏（Partial Sale）
批次事件（Batch Level）
栏位事件（Pen Level）
舍事件（Barn Level）

事件是实时滚动显示的数据源。

出栏（Sale / Buyer）
部分猪在达到销售标准后会出栏，数据记录：
buyer_name
出栏数量
关联 batch_id
出栏事件写入 event_log
buyer 逻辑：
buyer 相当于“一个简单的外部养殖场”
不分栏，但保留事件轨迹。

实验与免疫（Experiment / Vaccination）
免疫流程包括：
一免（1st vaccine）
二免（2nd vaccine）
留种逻辑：200 ~ 400 头留下育肥或留种
样本猪数量可变化（方案 A/B/C）
你给出的实例：
方案 A：疫苗足够 → 全部按计划进行（一免 + 二免）
方案 B：疫苗不足 → 部分猪只做 1 免，作为对照组出售
方案 C：疫苗更少 → 全部只做 1 免，不做 2 免

免疫方案影响批次批量逻辑与实验参数。

UI 逻辑（卡片式可视化）
FarmCard → 展示全场状态（数量、即将进行操作、事件滚动）
BarnCard → 展示猪舍数量、事件、类型（育肥/母猪/哺乳…）
PenCard → 展示栏状态、批次、数量、事件滚动
BatchCard → 展示批次细节、转舍轨迹、免疫状态
结构为逐层展开：
FarmCard → BarnCards → PenCards → BatchCards → Detail

大屏模式（PanelMode）
FarmCard (top)
SummaryRow
事件滚动栏
BarnGrid （平铺所有猪舍卡片）

项目状态（PROJECT STATUS）：
2) FIELDOPS_PROJECT_STATUS.txt
（我们已经做了什么 / 目前进度 / API 状态）

============================================================
FieldOps 项目进度文档
版本：2026-02

一、当前状态（2026/02）

FieldOps 独立系统已建立
目录：mms/FieldOps/
包含：
main.py
router.py
router_views.py
router_rewrite.py
router_api（待进一步完善）
views/
static/
schemas/
services/
models/

HTML 模板迁移成功
所有 legacy farm_domain 和 field_ops 下的 HTML 已复制到：
mms/FieldOps/views/farm_domain/
mms/FieldOps/views/field_ops/components/
mms/FieldOps/views/field_ops/pages/

静态资源加载成功
/static/css/style.css 正常工作

UI 主页面可用
FieldOps 首页（Dashboard）已加载成功
Farm Tree、Batch Detail、Event Trace、Inbound Wizard 页面可渲染

URL 重写器已生效
/pig-farm/* → 自动跳转到 /FieldOps/*

Jinja Loader 已修复
farm/* include 已正确重写到 views/farm_domain

二、后端 API 进度

Tree API（规划完成，模型结构已获取）
Batch API（未生成）
Pen API（未生成）
Barn API（未生成）
Event API（未生成）
Experiment API（未生成）
三、待办工作

基于 PigBatchLocation 重建 Tree API（下一阶段）
生成 Barn/Pen/Batch/Event 的 models + services + API
完成卡片 UI 的动态数据绑定
实现事件滚动 EventScroller API
实现免疫/实验方案 API
##实例:
产房共7舍,每个舍16栏,装猪只装15个,每栏15`16头猪,其中一个栏预留作为治疗,疗养用;保育共6舍,一个舍16栏,每栏1820头猪;育肥共7舍,15舍叫育肥舍,一个舍12圈,一栏20头猪,其中10栏装猪,2栏预留作为留观疗养; 6舍7舍叫二保育,每个舍12栏,一个栏30个猪,10栏装猪,2栏不装,也是预留作为治疗栏;目前的600头,在保育的5舍,6舍,一栏20头,共600头; 今天下午转至二保育,6舍,7舍,一舍300头. 预计下2月2日至8日之间进1500头,1213日进1500,不是之前的2200头了,这些猪预计进行一免,其中200400头在销售最终会留下来,进行留种或育肥,留下来的猪做2免;目前有个问题是实验疫苗的数量,如果本次生产的数量足够,就全都按计划进行,这个叫方案A,如果疫苗数量不够,需要方案B, 在保证600头二免的情况下,一部分猪,不做1免,直接作为对照组,销售掉;方案C,全部只做1免,不做2免;这个数量是根据疫苗实际生产数量来定的,目前可能会是3个范围,2900头份,3600头份或5000头份

Agent 知识库（AGENT KNOWLEDGE）：
3) FIELDOPS_AGENT_KNOWLEDGE.txt
（agent 的当前知识库 / 主要模块 / 可执行任务）

============================================================
FieldOps Agent 知识库
版本：2026-02

一、Agent 范围与能力

可以创建/改写 mms/FieldOps 内的文件

可以复制 legacy 文件到 FieldOps

可以生成：

HTML 模板
API 路由
Service 层
Schemas
Data Models
Jinja Loader 配置
URL Rewrite 规则
可以生成调试脚本（debug_fieldops_routes.py）

可以生成技术文档

可以执行结构迁移任务

不会修改 mms_legacy 下任何文件（严格只读）

二、已知路径

FieldOps 目录：
mms/FieldOps/

Legacy HTML：
mms_legacy/templates/farm_domain/
mms_legacy/templates/field_ops/pages/
mms_legacy/templates/field_ops/components/

Legacy Models：
mms_legacy/app/models/pig_batches.py
mms_legacy/app/models/pig_batch_events.py
mms_legacy/app/models/pig_batch_locations.py

三、Agent 当前用于 FieldOps 的固定模板
router.py
router_views.py
router_rewrite.py
main.py
base.html
index.html

四、Agent 未来任务

生成 Tree API
生成 Barn/Pen/Batch/Event API
生成 Experiment API
自动解析 HTML 提取页面参数
自动生成 schemas/models
自动绑定页面 AJAX/fetch 请求

四、当前已完成内容（必须知晓）
1. FieldOps 独立子系统已建立：mms/FieldOps/
2. 所有 FARM/FieldOps HTML 已复制到 FieldOps/views/ 下
3. 所有页面 farm-tree、farm-structure、batch-detail、event-trace、inbound-wizard 均可 200 OK 渲染
4. 静态 CSS 成功加载
5. 旧系统 /pig-farm/* 路径已自动跳转到 /FieldOps/*
6. Jinja Loader 已修复，可正确加载 farm/ 与 field_ops/ includes

五、下一位必须继续的开发任务
1. 生成 FieldOps 后端真实 API：
   /FieldOps/api/tree
   /FieldOps/api/batches
   /FieldOps/api/barn/{id}
   /FieldOps/api/pen/{id}
   /FieldOps/api/events
   /FieldOps/api/experiment

2. 将 API 与前端卡片 UI 联动

3. 生成事件滚动事件流 EventScroller

4. 生成免疫实验（方案 A/B/C）流程 API

5. 生成完整 models/schemas/services

六、业务核心逻辑（摘要）
位置体系：
Farm → Barn(带类型) → Pen → Batch 分布 → Events

事件体系：
转栏、死亡、出栏、防疫、生病、治疗、批次事件、栏事件、舍事件

批次体系：
一次进场 N 头 → 多栏分布 → 事件驱动流转

免疫体系：
1 免、2 免、留种逻辑、实验方案 A/B/C

七、接手流程（必须遵守）
1. 加载三份文档
2. 阅读当前项目状态
3. 从未完成列表依序推进
4. 所有后端代码写入 mms/FieldOps/
5. legacy 只读
6. 使用 mms_agent 执行 DSL
7. 维持 FieldOps 为独立子系统

（任务卡结束）