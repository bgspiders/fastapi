# API信息查看平台

一个基于FastAPI构建的接口平台，用于查看请求的IP地址、Headers等信息。

## 功能特性

- 🌐 **IP地址检测**: 支持多种代理环境下的真实IP获取
- 📋 **Headers查看**: 完整的HTTP请求头信息展示
- 🕵️ **User-Agent解析**: 自动解析浏览器、操作系统、设备类型
- 🔄 **请求回显**: POST请求数据回显功能
- 📖 **自动文档**: 集成Swagger UI自动生成API文档
- 🎨 **美观界面**: 现代化的Web界面，支持在线测试

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python main.py
```

或者使用uvicorn直接启动：

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### 3. 访问平台

- **主页**: http://localhost:8080
- **API文档**: http://localhost:8080/docs
- **ReDoc文档**: http://localhost:8080/redoc

## API接口

### 1. 获取完整请求信息
```
GET /info
```
返回当前请求的完整信息，包括IP、Headers、参数等。

### 2. 获取IP地址
```
GET /ip
```
仅返回客户端IP地址信息。

### 3. 获取请求头
```
GET /headers
```
返回所有HTTP请求头信息。

### 4. 获取User-Agent信息
```
GET /user-agent
```
返回User-Agent信息及解析结果。

### 5. 请求回显
```
POST /echo
```
回显POST请求的数据。

## 响应示例

### /info 接口响应
```json
{
    "timestamp": "2024-01-01T12:00:00",
    "client_ip": "192.168.1.100",
    "method": "GET",
    "url": "http://localhost:8080/info",
    "headers": {
        "user-agent": "Mozilla/5.0...",
        "accept": "application/json",
        "host": "localhost:8080"
    },
    "query_params": {},
    "path_params": {},
    "cookies": {},
    "client": {
        "host": "127.0.0.1",
        "port": 54321
    }
}
```

### /ip 接口响应
```json
{
    "timestamp": "2024-01-01T12:00:00",
    "client_ip": "192.168.1.100",
    "real_ip": null,
    "forwarded_for": null,
    "forwarded": null,
    "client_host": "127.0.0.1"
}
```

## IP地址检测机制

平台支持多种代理环境下的真实IP获取：

1. **X-Forwarded-For**: 最常见的代理头
2. **X-Real-IP**: Nginx等代理服务器使用的头
3. **X-Forwarded**: 标准代理头
4. **客户端IP**: 直接连接的客户端IP

## 技术栈

- **FastAPI**: 现代、快速的Web框架
- **Uvicorn**: ASGI服务器
- **Pydantic**: 数据验证
- **HTML/CSS/JavaScript**: 前端界面

## 部署说明

### 开发环境
```bash
python main.py
```

### 生产环境
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```

### Docker部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## 许可证

MIT License 