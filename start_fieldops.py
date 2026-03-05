import sys
import os

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 确保 mms 目录在路径中
mms_path = os.path.join(project_root, 'mms')
sys.path.insert(0, mms_path)

# 从 mms.main 启动应用（绝对导入）
from mms.main import app

if __name__ == "__main__":
    # 启动 Uvicorn
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)