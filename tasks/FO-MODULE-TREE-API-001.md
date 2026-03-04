FieldOps Agent 任务卡
Task-ID: FO-MODULE-TREE-API-001
任务类型: 后端 API 模块开发
系统: MMS FieldOps 子系统

一、任务范围
本任务只允许读写以下目录：
mms/FieldOps/

以下目录禁止修改（只读）：
mms_legacy/

二、任务目标
创建 FieldOps 位置树 Tree API。
完成后端真实 API：
GET /FieldOps/api/tree

实现以下文件（如不存在则创建）：
mms/FieldOps/router_api/tree.py
mms/FieldOps/services/tree_service.py
mms/FieldOps/schemas/tree_schema.py
mms/FieldOps/models/tree_model.py（如需要）
将路由注册到 FieldOps 主 router 与 main.py。

API 应返回：Farm → Barn → Pen → Batch 的完整层级结构。

三、业务需求要点
Farm（养殖场）
Barn（猪舍，带 type）
Pen（猪栏，带 capacity，可含治疗/预留栏）
Batch（批次，可分布到多个 Pen）
Batch 包含字段：batch_id、quantity

Tree API 输出格式要求：
farm:
barns[]:
barn_id
name
type
pens[]:
pen_id
capacity
batches[]:
batch_id
quantity

四、数据来源
使用 legacy 数据模型（只读）：
mms_legacy/app/models/pig_batch_locations.py
mms_legacy/app/models/pig_batches.py
mms_legacy/app/models/pig_batch_events.py

Tree API 主要依赖 pig_batch_locations：
farm → barn → pen → batch → quantity

五、开发步骤
新建 router_api/tree.py

创建路由 GET /FieldOps/api/tree
调用 tree_service.get_full_tree()
新建 services/tree_service.py

从 legacy models 读取所有 batch-location 信息
构建 Farm → Barn → Pen → Batch 的树状结构
返回 dict
新建 schemas/tree_schema.py

定义 FarmSchema、BarnSchema、PenSchema、BatchSchema
用于标准化响应 JSON
新建 models/tree_model.py（如需要）

定义内部数据结构
不修改 legacy 文件
注册路由

更新 router_api/init.py
更新 FieldOps/main.py
（可选）生成调试脚本 debug_fieldops_tree.py

打印 API 结果方便验证
六、完成标准
访问 /FieldOps/api/tree 返回真实、正确、结构化 JSON：
包含所有 barns、pens、batches
数量准确
无硬编码
不修改 legacy