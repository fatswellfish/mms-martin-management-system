# FieldOps Agent 知识库
版本：2026-02

## 一、Agent 范围与能力
- 可以创建/改写 `mms/FieldOps` 内的文件
- 可以复制 legacy 文件到 FieldOps
- 可以生成：
  - HTML 模板
  - API 路由
  - Service 层
  - Schemas
  - Data Models
  - Jinja Loader 配置
  - URL Rewrite 规则
- 可以生成调试脚本（`debug_fieldops_routes.py`）
- 可以生成技术文档
- 可以执行结构迁移任务
- **不会修改 `mms_legacy` 下任何文件**（严格只读）

## 二、已知路径
- **FieldOps 目录**：
  - `mms/FieldOps/`
- **Legacy HTML**：
  - `mms_legacy/templates/farm_domain/`
  - `mms_legacy/templates/field_ops/pages/`
  - `mms_legacy/templates/field_ops/components/`
- **Legacy Models**：
  - `mms_legacy/app/models/pig_batches.py`
  - `mms_legacy/app/models/pig_batch_events.py`
  - `mms_legacy/app/models/pig_batch_locations.py`

## 三、Agent 当前用于 FieldOps 的固定模板
- `router.py`
- `router_views.py`
- `router_rewrite.py`
- `main.py`
- `base.html`
- `index.html`

## 四、Agent 未来任务
- 生成 Tree API
- 生成 Barn/Pen/Batch/Event API
- 生成 Experiment API
- 自动解析 HTML 提取页面参数
- 自动生成 schemas/models
- 自动绑定页面 AJAX/fetch 请求

## 五、当前已完成内容（必须知晓）
1. FieldOps 独立子系统已建立：`mms/FieldOps/`
2. 所有 FARM/FieldOps HTML 已复制到 `FieldOps/views/` 下
3. 所有页面 `farm-tree`、`farm-structure`、`batch-detail`、`event-trace`、`inbound-wizard` 均可 200 OK 渲染
4. 静态 CSS 成功加载
5. 旧系统 `/pig-farm/*` 路径已自动跳转到 `/FieldOps/*`
6. Jinja Loader 已修复，可正确加载 `farm/` 与 `field_ops/` includes

## 六、下一位必须继续的开发任务
1. 生成 FieldOps 后端真实 API：
   - `/FieldOps/api/tree`
   - `/FieldOps/api/batches`
   - `/FieldOps/api/barn/{id}`
   - `/FieldOps/api/pen/{id}`
   - `/FieldOps/api/events`
   - `/FieldOps/api/experiment`
2. 将 API 与前端卡片 UI 联动
3. 生成事件滚动事件流 EventScroller
4. 生成免疫实验（方案 A/B/C）流程 API
5. 生成完整 models/schemas/services

## 七、业务核心逻辑（摘要）
- **位置体系**：
  - Farm → Barn(带类型) → Pen → Batch 分布 → Events
- **事件体系**：
  - 转栏、死亡、出栏、防疫、生病、治疗、批次事件、栏事件、舍事件
- **批次体系**：
  - 一次进场 N 头 → 多栏分布 → 事件驱动流转
- **免疫体系**：
  - 1 免、2 免、留种逻辑、实验方案 A/B/C

## 八、接手流程（必须遵守）
1. 加载三份文档（业务、状态、知识库）
2. 阅读当前项目状态
3. 从未完成列表依序推进
4. 所有后端代码写入 `mms/FieldOps/`
5. legacy 只读
6. 使用 `mms_agent` 执行 DSL
7. 维持 FieldOps 为独立子系统