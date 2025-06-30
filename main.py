from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any
import json
from datetime import datetime, date
import calendar
from holiday_loader import holiday_loader

app = FastAPI(
    title="API信息查看平台",
    description="一个用于查看请求IP地址、Headers等信息的API平台",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_time_info() -> Dict[str, Any]:
    """获取详细的时间信息"""
    now = datetime.now()
    today = now.date()
    
    # 使用新的节假日加载器
    holiday_info = holiday_loader.get_holiday_info(today)
    
    # 获取农历信息（简化版）
    lunar_info = get_lunar_date(today)
    
    return {
        "timestamp": now.isoformat(),
        "date": today.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": "Asia/Shanghai",
        "weekday": holiday_info["weekday"],
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "microsecond": now.microsecond,
        "is_holiday": holiday_info["is_holiday"],
        "is_workday": holiday_info["is_workday"],
        "holiday_name": holiday_info["holiday_name"],
        "holiday_type": holiday_info["holiday_type"],
        "holiday_source": holiday_info["source"],
        "lunar_date": lunar_info,
        "season": get_season(now.month),
        "quarter": (now.month - 1) // 3 + 1,
        "day_of_year": now.timetuple().tm_yday,
        "week_of_year": now.isocalendar()[1]
    }

def get_lunar_date(solar_date: date) -> Dict[str, Any]:
    """获取农历日期信息（简化版）"""
    # 这里使用简化的农历计算，实际项目中可以使用专门的农历库
    # 如 chinese_calendar 或 lunar_python
    
    # 简化实现：返回基本信息
    return {
        "lunar_year": "甲辰年",  # 2024年
        "lunar_month": "五月",
        "lunar_day": "十五",
        "zodiac": "龙",
        "festival": get_lunar_festival(solar_date)
    }

def get_lunar_festival(solar_date: date) -> str:
    """获取农历节日"""
    month = solar_date.month
    day = solar_date.day
    
    festivals = {
        (1, 1): "元旦",
        (2, 10): "春节",
        (4, 4): "清明节",
        (5, 1): "劳动节",
        (6, 10): "端午节",
        (9, 15): "中秋节",
        (10, 1): "国庆节",
    }
    
    return festivals.get((month, day), "")

def get_season(month: int) -> str:
    """获取季节"""
    if month in [3, 4, 5]:
        return "春季"
    elif month in [6, 7, 8]:
        return "夏季"
    elif month in [9, 10, 11]:
        return "秋季"
    else:
        return "冬季"

@app.get("/", response_class=HTMLResponse)
async def root():
    """主页 - 显示API使用说明"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API信息查看平台</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 30px;
                margin: 20px 0;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #fff;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .api-section {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 20px;
                margin: 15px 0;
                border-left: 4px solid #4CAF50;
            }
            .endpoint {
                background: rgba(0, 0, 0, 0.2);
                padding: 10px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                margin: 10px 0;
            }
            .method {
                color: #4CAF50;
                font-weight: bold;
            }
            .url {
                color: #2196F3;
            }
            .description {
                color: #FFC107;
                font-style: italic;
            }
            .test-button {
                background: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin: 5px;
                font-size: 14px;
            }
            .test-button:hover {
                background: #45a049;
            }
            .docs-link {
                text-align: center;
                margin-top: 30px;
            }
            .docs-link a {
                color: #FFC107;
                text-decoration: none;
                font-size: 18px;
            }
            .docs-link a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 API信息查看平台</h1>
            
            <div class="api-section">
                <h2>📡 可用接口</h2>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/info</span>
                    <div class="description">获取当前请求的完整信息（IP、Headers、请求参数等）</div>
                    <button class="test-button" onclick="testEndpoint('/info')">测试接口</button>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/ip</span>
                    <div class="description">仅获取客户端IP地址</div>
                    <button class="test-button" onclick="testEndpoint('/ip')">测试接口</button>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/headers</span>
                    <div class="description">获取所有请求头信息</div>
                    <button class="test-button" onclick="testEndpoint('/headers')">测试接口</button>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/user-agent</span>
                    <div class="description">获取User-Agent信息</div>
                    <button class="test-button" onclick="testEndpoint('/user-agent')">测试接口</button>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/time</span>
                    <div class="description">获取时间信息和节假日判断</div>
                    <button class="test-button" onclick="testEndpoint('/time')">测试接口</button>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/echo</span>
                    <div class="description">回显POST请求的数据</div>
                    <button class="test-button" onclick="testPostEndpoint()">测试接口</button>
                </div>
            </div>
            
            <div class="api-section">
                <h2>📋 响应示例</h2>
                <pre style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 5px; overflow-x: auto;">
{
    "timestamp": "2024-01-01T12:00:00",
    "client_ip": "192.168.1.100",
    "headers": {
        "user-agent": "Mozilla/5.0...",
        "accept": "application/json",
        "host": "localhost:8080"
    },
    "method": "GET",
    "url": "http://localhost:8080/info"
}
                </pre>
            </div>
            
            <div class="docs-link">
                <a href="/docs" target="_blank">📖 查看完整API文档 (Swagger UI)</a>
            </div>
        </div>
        
        <script>
            async function testEndpoint(endpoint) {
                try {
                    const response = await fetch(endpoint);
                    const data = await response.json();
                    alert('响应数据:\\n' + JSON.stringify(data, null, 2));
                } catch (error) {
                    alert('请求失败: ' + error.message);
                }
            }
            
            async function testPostEndpoint() {
                try {
                    const response = await fetch('/echo', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: 'Hello from client!',
                            timestamp: new Date().toISOString()
                        })
                    });
                    const data = await response.json();
                    alert('响应数据:\\n' + JSON.stringify(data, null, 2));
                } catch (error) {
                    alert('请求失败: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/info")
async def get_request_info(request: Request):
    """获取完整的请求信息"""
    client_ip = get_client_ip(request)
    
    info = {
        "timestamp": datetime.now().isoformat(),
        "client_ip": client_ip,
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "path_params": request.path_params,
        "cookies": request.cookies,
        "client": {
            "host": request.client.host if request.client else None,
            "port": request.client.port if request.client else None,
        }
    }
    
    return info

@app.get("/ip")
async def get_ip(request: Request):
    """仅获取客户端IP地址"""
    client_ip = get_client_ip(request)
    return {
        "timestamp": datetime.now().isoformat(),
        "client_ip": client_ip,
        "real_ip": request.headers.get("x-real-ip"),
        "forwarded_for": request.headers.get("x-forwarded-for"),
        "forwarded": request.headers.get("x-forwarded"),
        "client_host": request.client.host if request.client else None
    }

@app.get("/headers")
async def get_headers(request: Request):
    """获取所有请求头信息"""
    return {
        "timestamp": datetime.now().isoformat(),
        "headers": dict(request.headers),
        "total_headers": len(request.headers)
    }

@app.get("/user-agent")
async def get_user_agent(request: Request):
    """获取User-Agent信息"""
    user_agent = request.headers.get("user-agent", "Unknown")
    return {
        "timestamp": datetime.now().isoformat(),
        "user_agent": user_agent,
        "parsed_info": parse_user_agent(user_agent)
    }

@app.get("/time")
async def get_time():
    """获取时间信息和节假日判断"""
    return get_time_info()

@app.get("/time/{date_str}")
async def get_time_by_date(date_str: str):
    """根据指定日期获取时间信息和节假日判断"""
    try:
        # 解析日期字符串
        check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        now = datetime.now()
        
        # 获取节假日信息
        holiday_info = holiday_loader.get_holiday_info(check_date)
        
        # 获取农历信息
        lunar_info = get_lunar_date(check_date)
        
        return {
            "query_date": date_str,
            "current_time": now.isoformat(),
            "date": check_date.strftime("%Y-%m-%d"),
            "weekday": {
                "number": check_date.weekday(),
                "name": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][check_date.weekday()],
                "english": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][check_date.weekday()]
            },
            "is_holiday": holiday_info["is_holiday"],
            "is_workday": holiday_info["is_workday"],
            "holiday_name": holiday_info["holiday_name"],
            "holiday_type": holiday_info["holiday_type"],
            "holiday_source": holiday_info["source"],
            "lunar_date": lunar_info,
            "season": get_season(check_date.month),
            "quarter": (check_date.month - 1) // 3 + 1,
            "day_of_year": check_date.timetuple().tm_yday,
            "week_of_year": check_date.isocalendar()[1]
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD 格式")

@app.get("/holiday/years")
async def get_available_years():
    """获取可用的节假日数据年份"""
    return {
        "available_years": holiday_loader.get_available_years(),
        "total_years": len(holiday_loader.get_available_years())
    }

@app.get("/holiday/{year}")
async def get_year_holidays(year: int):
    """获取指定年份的所有节假日信息"""
    try:
        holidays = holiday_loader.get_year_holidays(year)
        return {
            "year": year,
            "total_days": len(holidays),
            "holidays": holidays,
            "holiday_count": len([h for h in holidays if h["is_holiday"]]),
            "workday_count": len([h for h in holidays if h["is_workday"]])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获取节假日数据失败: {str(e)}")

@app.get("/holiday/check/{date_str}")
async def check_holiday(date_str: str):
    """检查指定日期是否为节假日"""
    try:
        check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        holiday_info = holiday_loader.is_holiday(check_date)
        
        return {
            "date": date_str,
            "is_holiday": holiday_info["is_holiday"],
            "is_workday": holiday_info["is_workday"],
            "holiday_name": holiday_info["holiday_name"],
            "type": holiday_info["type"],
            "source": holiday_info["source"]
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，请使用 YYYY-MM-DD 格式")

@app.post("/echo")
async def echo_request(request: Request):
    """回显POST请求的数据"""
    try:
        body = await request.body()
        content_type = request.headers.get("content-type", "")
        
        if "application/json" in content_type:
            json_data = await request.json()
            data = {"json_data": json_data}
        else:
            data = {"raw_data": body.decode()}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "method": request.method,
            "content_type": content_type,
            "content_length": len(body),
            "data": data,
            "headers": dict(request.headers)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"无法解析请求数据: {str(e)}")

def get_client_ip(request: Request) -> str:
    """获取客户端真实IP地址"""
    # 检查各种可能的IP头
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip
    
    forwarded = request.headers.get("x-forwarded")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    # 如果没有代理头，使用客户端IP
    if request.client:
        return request.client.host
    
    return "unknown"

def parse_user_agent(user_agent: str) -> Dict[str, Any]:
    """简单解析User-Agent信息"""
    info = {
        "browser": "Unknown",
        "os": "Unknown",
        "device": "Unknown"
    }
    
    user_agent_lower = user_agent.lower()
    
    # 浏览器检测
    if "chrome" in user_agent_lower:
        info["browser"] = "Chrome"
    elif "firefox" in user_agent_lower:
        info["browser"] = "Firefox"
    elif "safari" in user_agent_lower:
        info["browser"] = "Safari"
    elif "edge" in user_agent_lower:
        info["browser"] = "Edge"
    elif "opera" in user_agent_lower:
        info["browser"] = "Opera"
    
    # 操作系统检测
    if "windows" in user_agent_lower:
        info["os"] = "Windows"
    elif "mac" in user_agent_lower:
        info["os"] = "macOS"
    elif "linux" in user_agent_lower:
        info["os"] = "Linux"
    elif "android" in user_agent_lower:
        info["os"] = "Android"
    elif "ios" in user_agent_lower:
        info["os"] = "iOS"
    
    # 设备类型检测
    if "mobile" in user_agent_lower or "android" in user_agent_lower or "iphone" in user_agent_lower:
        info["device"] = "Mobile"
    elif "tablet" in user_agent_lower or "ipad" in user_agent_lower:
        info["device"] = "Tablet"
    else:
        info["device"] = "Desktop"
    
    return info

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 