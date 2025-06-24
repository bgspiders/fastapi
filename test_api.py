#!/usr/bin/env python3
"""
API信息查看平台测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_endpoint(endpoint, method="GET", data=None):
    """测试API端点"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        print(f"\n🔍 测试 {method} {endpoint}")
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📋 响应数据:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"❌ 错误: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ 连接失败: 请确保服务已启动在 {BASE_URL}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def main():
    """主测试函数"""
    print("🧪 API信息查看平台测试")
    print("=" * 50)
    
    # 测试各个端点
    endpoints = [
        ("/info", "GET"),
        ("/ip", "GET"),
        ("/headers", "GET"),
        ("/user-agent", "GET"),
    ]
    
    for endpoint, method in endpoints:
        test_endpoint(endpoint, method)
        time.sleep(1)  # 避免请求过快
    
    # 测试POST端点
    test_data = {
        "message": "Hello from test script!",
        "timestamp": time.time(),
        "test": True
    }
    test_endpoint("/echo", "POST", test_data)
    
    print("\n✅ 测试完成!")
    print(f"🌐 访问主页: {BASE_URL}")
    print(f"📖 查看API文档: {BASE_URL}/docs")

if __name__ == "__main__":
    main() 