写入文件 docs/FIELDOPS_AGENT_KNOWLEDGE.txt；
内容为：
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
