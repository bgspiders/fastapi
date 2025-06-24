from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any
import json
from datetime import datetime

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
        "host": "localhost:8000"
    },
    "method": "GET",
    "url": "http://localhost:8000/info"
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
        port=8000,
        reload=True,
        log_level="info"
    ) 