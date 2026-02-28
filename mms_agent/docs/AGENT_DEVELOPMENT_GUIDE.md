# MMS Agent - Development Guide

本文件提供给未来维护 MMS Agent 的开发者参考。

-----------------------------------------
# 1. 架构思想
-----------------------------------------

MMS Agent 是一个“工程自动化引擎”（Engineering Automation Engine）。  
它不是业务模块，而是独立的工程开发辅助系统。

它由三层组成：

- CLI（dev_agent.py）：任务入口 + DSL 执行器
- Agent Core（agent/*.py）：权限、路径、扫描、定位
- Extension Engine（refactor_engine/, migrator/）：自动重构 & 拆分

-----------------------------------------
# 2. 如何扩展 DSL
-----------------------------------------

dev_agent.py 的 DSLInterpreter 负责解析 DSL。

要扩展新指令：

1. 在 DSLInterpreter.run() 中添加新指令识别
2. 实现对应的 `_xxx` 方法
3. 在文档中添加说明
4. 更新 agent_scope 权限检查

-----------------------------------------
# 3. 如何扩展权限系统
-----------------------------------------

当前权限系统基于：

agent_scope.py

TEXT

未来可以升级至：

- JSON 配置文件（scope.json）
- Web UI 配置界面（/agent/scope）
- 多项目支持

-----------------------------------------
# 4. 如何扩展自动重构能力
-----------------------------------------

refactor_engine 提供：

- analyzer（AST 分析）
- classifier（分类器）
- splitter（拆分类）
- writer（文件编写）

如需扩展：

- 修改 config.py 添加关键字
- 修改 classifier 实现新的分类策略
- 修改 writer 输出新的层结构（如 domain/ui/repository）

-----------------------------------------
# 5. 如何扩展 Web UI（未来 Phase C）
-----------------------------------------

建议使用 FastAPI + HTMX：

GET /agent/dashboard
GET /agent/scope
POST /agent/scope/update
POST /agent/run-task

TEXT

该 UI 仅供 Agent 使用，不暴露给生产系统。

-----------------------------------------
# 6. Agent 的设计原则
-----------------------------------------

- 不修改 legacy —— 只读  
- 不破坏执行环境  
- DSL 必须可读、可维护  
- 权限必须安全  
- 所有写操作必须可追踪  
- 一次执行一个任务文件  
- 每次升级必须同步文档更新  