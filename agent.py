import os
import subprocess
import json
from pathlib import Path
import ollama

MODEL = "qwen2.5-coder:latest"
PROJECT_DIR = Path(__file__).parent.resolve()

SYSTEM_PROMPT = """
你是一个本地运行的自主软件工程师（Goal-driven Agent）。

你的能力包括（必须执行）：
- 分析用户目标
- 自主规划任务（多步骤）
- 使用 ReAct 思考（思考 → 行动 → 观察 → 再思考）
- 若命令失败，自动尝试替代方案（例如 Windows 下用 dir 替代 ls）
- 自动读取文件内容
- 自动列出目录结构（不依赖 shell 命令）
- 自动总结结果
- 自动反思错误原因并修正行动策略
- 自动推进到完成目标为止

使用下面这些工具：

【工具1：目录列表】
格式：
<tool:list_dir path="相对路径"></tool>

【工具2：读取文件】
格式：
<tool:read_file path="相对路径"></tool>

【工具3：执行命令】
格式：
<tool:run>
命令
</tool:run>

使用 ReAct 输出格式：

<thought>
你的思考，包括：
- 当前目标
- 为什么这样行动
- 下一步计划
</thought>

<action>
（使用上述工具之一）
</action>

当你认为任务完成，用：
<final>
（总结结果）
</final>

绝对不要在没有说明理由的情况下停止。
你的策略是：失败 → 反思 → 换方法 → 再行动。
"""

def ask_llm(messages):
    """调用本地 Qwen"""
    resp = ollama.chat(
        model=MODEL,
        messages=messages,
        stream=False
    )
    return resp["message"]["content"]

def tool_list_dir(path):
    """列出目录内容（不依赖 shell 命令）"""
    target = (PROJECT_DIR / path).resolve()
    if not target.exists():
        return f"[错误] 目录不存在: {path}"
    if not target.is_dir():
        return f"[错误] 不是目录: {path}"

    items = []
    for x in target.iterdir():
        t = "DIR" if x.is_dir() else "FILE"
        items.append(f"{t} - {x.name}")
    return "\n".join(items)

def tool_read_file(path):
    target = (PROJECT_DIR / path).resolve()
    if not target.exists():
        return f"[错误] 文件不存在: {path}"
    if not target.is_file():
        return f"[错误] 不是文件: {path}"

    with open(target, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def tool_run(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    return result.stdout + result.stderr

def execute_action(block):
    """解析并执行行动"""
    if block.startswith("<tool:list_dir"):
        start = block.find('path="') + 6
        end = block.find('"', start)
        path = block[start:end]
        return tool_list_dir(path)

    if block.startswith("<tool:read_file"):
        start = block.find('path="') + 6
        end = block.find('"', start)
        path = block[start:end]
        return tool_read_file(path)

    if block.startswith("<tool:run>"):
        cmd = block[10:-11].strip()
        return tool_run(cmd)

    return "[错误] 未知工具调用"

def extract_actions(text):
    actions = []
    while True:
        start = text.find("<tool:")
        if start == -1:
            break
        end = text.find("</tool", start)
        block_end = text.find(">", end) + 1
        actions.append(text[start:block_end])
        text = text[block_end:]
    return actions

def main():
    print("[AGENT] 本地自主工程师已启动")
    print("[AGENT] 项目目录:", PROJECT_DIR)
    user_goal = input("你的目标任务： ")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"项目目录：{PROJECT_DIR}\n目标：{user_goal}"}
    ]

    for step in range(1, 20):  # 最多20步
        print(f"\n===== 第 {step} 步推理 =====\n")

        reply = ask_llm(messages)
        print(reply)

        # 是否任务完成？
        if "<final>" in reply:
            print("\n===== 任务完成 =====\n")
            return

        # 提取行动
        actions = extract_actions(reply)
        if not actions:
            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "user", "content": "未找到行动，请反思并继续下一步"})
            continue

        # 执行第一条行动
        action = actions[0]
        result = execute_action(action)

        print("\n===== 执行动作结果 =====\n")
        print(result)

        # 反馈给 LLM 继续下一轮
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"动作结果：\n{result}\n请根据结果反思并继续。"})

    print("[AGENT] 超出最大步数，停止。")


if __name__ == "__main__":
    main()
