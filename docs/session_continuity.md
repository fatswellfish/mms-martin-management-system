# MMS 项目会话衔接保障方案

## 核心原则：以 `tasks/` 为唯一执行入口，以 `docs/` 为唯一决策依据。

### 1. 会话重启时的自动恢复流程 (自动化)
- **步骤一**: 新会话启动后，系统将自动读取 `tasks/` 目录下的所有文件（如 `task1.md`, `task2.md`, `plan.md`）。
- **步骤二**: 系统会**优先检查 `tasks/` 中是否存在一个名为 `current_step.md` 的文件**。
  - **如果存在**: 系统将立即加载该文件内容，并以此作为当前任务的上下文，无缝接续上一次中断的工作。
  - **如果不存在**: 系统将根据 `plan.md` 的指导，从第一步开始执行。

### 2. 会话切换时的主动同步机制 (手动控制)
- **每次完成一个任务步骤后**，在输出最终结果前，必须执行以下操作：
  1.  **创建/更新 `tasks/current_step.md`**: 将当前已完成的任务描述、已生成的文件列表和下一步计划写入此文件。例如：
      ```markdown
      ## 步骤: 1/3 - 创建 fieldops 模型层
      - 已完成: `mms/modules/fieldops/models/location.py`, `mms/modules/fieldops/schemas/location.py`
      - 下一步: 开发 `models/batch.py` 和 `schemas/batch.py`
      ```
  2.  **在回复中明确声明**：
      > `【状态更新】任务已推进至步骤1，详细记录在 `tasks/current_step.md`。下次会话可直接从这里继续。`

### 3. 会话交接时的验证清单 (建议用户使用)
当您需要在不同会话间交接工作时，请确保以下事项：
- ✅ `tasks/` 目录下存在 `current_step.md`。
- ✅ `current_step.md` 中包含清晰的进度描述和下一步计划。
- ✅ `docs/` 目录下的 `system_design.md` 和 `execution_constraints.md` 是最新的。

## 总结
通过将 `tasks/` 视为“执行日志”，将 `docs/` 视为“决策圣经”，并强制要求在每个步骤结束时更新 `current_step.md`，我们构建了一个高度可靠的无缝衔接机制。只要 `current_step.md` 存在且准确，任何新会话都能瞬间恢复到上次工作的精确位置。