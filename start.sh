#!/bin/bash

echo "🚀 启动API信息查看平台..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python"
    exit 1
fi

# 检查依赖是否安装
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 启动服务
echo "🌟 启动服务..."
echo "📍 访问地址: http://localhost:8080"
echo "📖 API文档: http://localhost:8080/docs"
echo "⏹️  按 Ctrl+C 停止服务"
echo ""

python main.py 