# MMS Agent - Overview

MMS Agent（mms_agent）是 MMS 系统的自动化工程助手。  
它是一个独立的工程，不属于 MMS 应用，也不属于业务模块。

Agent 的职责包括：

- 文件结构扫描
- 自动化任务执行（基于 DSL）
- 自动化生成目录/文件/代码
- 支持迁移 legacy 项目到新 MMS 架构
- 分析项目拓扑
- 重构与模块拆分（refactor engine）
- 未来提供 Web 管理 UI（Phase C - planned）

Agent 采用 DSL（Domain Specific Language）来执行任务文件。  
这为工程提供了极强的自动化能力，并允许未来扩展。

Agent 的权限系统位于：
project/mms_agent/agent/agent_scope.py


MMS Agent 支持三个权限层级：

- ALLOWED_ROOTS：允许修改的路径
- READ_ONLY：只允许读取，不允许修改
- DENY：完全禁止访问的路径

当前阶段（Phase A）使用 Python 文件作为权限来源。  
未来（Phase C）将提供 Web UI + JSON 的权限编辑界面。

Agent 执行任务文件的入口：

python dev_agent.py "执行任务文件 docs/XXX.md"


任务文件可以包含 DSL 指令，用于创建目录、写入文件、移动、复制等。

MMS Agent 是 MMS 架构迁移、扩展与自动化的核心工具。
