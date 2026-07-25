"""
GB/T 8567 国标注释
Web后端服务模块
核心能力：端口智能分配（优先6554，占用自动随机端口）、FastAPI路由、跨域配置、用户信息接口
"""
import socket

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.account.local_login import get_offline_user_info
from src.config.config_loader import config

app = FastAPI(title="FeatherPen 羽笔", version="1.0.0")

# 跨域中间件配置
if config["network"]["enable_cors"]:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def index_root():
    """服务根路由，返回基础服务信息"""
    return {
        "service_name": "FeatherPen",
        "version": "V1.0.0",
        "offline_uid": config["security"]["offline_fixed_uid"]
    }

@app.get("/api/v1/user/info")
def api_user_info():
    """获取当前离线用户完整信息接口"""
    return get_offline_user_info()

@app.post("/api/v1/user/check_name")
def api_check_username(username: str):
    """账号查重接口，校验用户名/邮箱全局唯一性"""
    from src.database.db_sqlite import get_db_conn
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM local_user WHERE uid = ?", (username,))
    is_exist = cur.fetchone() is not None
    return {"code": 200, "is_exist": is_exist, "msg": "账号已存在" if is_exist else "账号可用"}

def get_available_port(host: str, prefer_port: int) -> int:
    """
    端口分配策略
    1. 优先绑定指定首选端口6554
    2. 端口占用则由系统自动分配随机空闲端口
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, prefer_port))
            return prefer_port
    except OSError:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, 0))
            return sock.getsockname()[1]

def run_server():
    """启动Web服务入口函数"""
    host = config["network"]["bind_address"]
    prefer_port = config["network"]["preferred_port"]
    real_port = get_available_port(host, prefer_port)

    print("=" * 52)
    print("FeatherPen Web服务启动完成")
    print(f"本地访问地址：http://{host}:{real_port}")
    print(f"离线游客固定UID：{config['security']['offline_fixed_uid']}")
    if real_port != prefer_port:
        print(f"警告：首选端口{prefer_port}被占用，系统自动切换至{real_port}")
    print("=" * 52)

    uvicorn.run(
        app,
        host=host,
        port=real_port,
        log_level="warning"
    )
