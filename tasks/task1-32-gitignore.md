# mms/FieldOps/.gitignore
# FieldOps 项目 - Git 忽略文件（已完成）

# Python 编译文件
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
build/
develop-eggs.pth
installed-eggs.pth
*.egg-info/
*.egg-

# Virtual Environment
venv/
.env
.venv/
env.bak/

# IDE 配置文件
.idea/
.vscode/
*.swp
*.swo
*~

# Database 文件（仅限开发环境）
data/fieldops.db
*.sqlite
*.db

# Log 文件
logs/
*.log

# 编译产物（如前端构建输出）
static/dist/
static/build/
public/

# 环境变量文件（敏感信息）
.env.local
.env.development
.env.production
.env.example

# 临时文件
.DS_Store
Thumbs.db

# 前端构建缓存（如 Webpack）
node_modules/
package-lock.json
yarn.lock

# 模板生成的文件（避免提交）
*.template
*.tmp

# 敏感数据（防止误提交）
secrets/
keys/
passwords/
api_keys.txt

# 项目特定忽略（如测试数据）
test_data/
example_data/

# 保持以下文件在版本控制中：
# - .gitignore（本身）
# - README.md
# - LICENSE
# - tasks/*.md（任务卡与进度记录）
# - mms/FieldOps/*.py（核心代码）
# - mms/FieldOps/static/（前端资源）