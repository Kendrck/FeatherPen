# FeatherPen/src/server/http_server.py
"""
GB/T 8567 FastAPI离线后端服务模块
基准文档：docs/API_MODULE_SPEC.md
约束：删除调试JSON路由，日志仅输出error级别
"""

import uvicorn

from src import app

# 使用文档完整标准函数名，无简写错误
from src.config.config_loader import load_global_config


@app.get("/api/v1/ping")
async def service_health_check():
    """GUI专用健康检测接口，文档规定返回{"code":200}"""
    return {"code": 200}


def run_server() -> None:
    """阻塞启动后端服务"""
    cfg = load_global_config()
    host = cfg["network"]["bind_address"]
    port = cfg["network"]["preferred_port"]
    uvicorn.run(app, host=host, port=port, log_level="error")


__all__ = ["run_server"]
