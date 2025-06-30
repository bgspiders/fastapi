#!/usr/bin/env python3
"""
节假日功能测试脚本
"""

import requests
import json
from datetime import date, timedelta

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
    print("🎉 节假日功能测试")
    print("=" * 50)
    
    # 测试可用年份
    test_endpoint("/holiday/years")
    
    # 测试节假日检查
    test_dates = [
        "2024-01-01",  # 元旦
        "2024-02-10",  # 春节
        "2024-02-04",  # 春节调休
        "2024-05-01",  # 劳动节
        "2024-10-01",  # 国庆节
        "2024-12-25",  # 圣诞节（非中国法定节假日）
        "2024-12-28",  # 普通工作日
        "2024-12-29",  # 周末
    ]
    
    print("\n📅 测试节假日检查:")
    for test_date in test_dates:
        test_endpoint(f"/holiday/check/{test_date}")
    
    # 测试时间接口（包含节假日信息）
    print("\n⏰ 测试时间接口:")
    test_endpoint("/time")
    
    # 测试指定日期的时间接口
    print("\n📅 测试指定日期的时间接口:")
    for test_date in test_dates[:3]:  # 只测试前3个日期
        test_endpoint(f"/time/{test_date}")
    
    # 测试年份节假日数据
    print("\n📊 测试年份节假日数据:")
    test_endpoint("/holiday/2024")
    
    print("\n✅ 节假日功能测试完成!")
    print(f"🌐 访问主页: {BASE_URL}")
    print(f"📖 查看API文档: {BASE_URL}/docs")

if __name__ == "__main__":
    main() 