# MMS Agent - Internal Specification

本文件定义 MMS Agent 的内部行为规范，包括 DSL 指令、  
目录结构、执行流程、权限机制。

-----------------------------------------
# 1. Agent 目录结构
-----------------------------------------

project/
    mms_agent/
        dev_agent.py             ← 主入口
        agent/
            agent_scope.py       ← 权限控制
            project_context.py   ← 路径解析（预留）
            locator.py           ← 文件定位（预留）
            scan.py              ← 扫描器（预留）
            migrator/
            refactor_engine/
        docs/
            AGENT_OVERVIEW.md
            AGENT_INTERNAL_SPEC.md
            AGENT_DEVELOPMENT_GUIDE.md


-----------------------------------------
# 2. DSL 指令语法（Phase A）
-----------------------------------------

## 创建目录
创建目录 <path>；

TEXT

## 写入文件
写入文件 <path>；
内容为：
<任意文本>

TEXT

## 删除文件
删除文件 <path>；

TEXT

## 复制文件
复制文件 <src> → <dst>；

TEXT

## 移动文件
移动文件 <src> → <dst>；

TEXT

-----------------------------------------
# 3. 执行流程
-----------------------------------------

1. 用户写任务文件（docs/*.md）
2. 用户运行：
python dev_agent.py "执行任务文件 docs/xxx.md"

TEXT
3. dev_agent 解析任务文件
4. 对于每一行执行 DSL 解析
5. 执行前校验权限（agent_scope.validate_write）
6. 执行操作
7. 刷新 PROJECT_TREE.md
8. 输出日志


-----------------------------------------
# 4. 权限机制
-----------------------------------------

权限控制基于 agent_scope.py：

ALLOWED_ROOTS = [...]
READ_ONLY = [...]
DENY = [...]

TEXT

### 写操作执行流程：

validate_write(path)
→ 检查是否 DENY
→ 检查是否只读
→ 检查是否在 ALLOWED_ROOTS
→ 允许

TEXT

### 读操作流程：
validate_read(path)
→ 检查是否 DENY
→ 允许

TEXT

-----------------------------------------
# 5. 未来扩展（Phase B, Phase C）
-----------------------------------------

- Phase B：支持任务文件中的 IF/LOOP 控制结构  
- Phase C：Web UI 配置权限 & 执行任务  
- Phase C：JSON-based agent_scope  
- Phase C：动态模块加载  
- Phase C：任务调度器（pipeline）