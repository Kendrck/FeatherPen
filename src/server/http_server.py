# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 FastAPI后端服务启动模块
文件路径: FeatherPen/src/server/http_server.py
功能：初始化Web服务、挂载前端静态资源、登录业务接口、状态接口、端口自动分配
约束：根路由指向web首页；登录接口POST /api/v1/user/login；三层账号校验逻辑；仅本地127.0.0.1监听
"""
import socket
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.account.local_login import (
    OFFLINE_GUEST_UID,
    PRIVILEGE_UID_LIST,
    verify_local_account,
)
from src.account.member_ctrl import _get_member_config
from src.config.config_loader import config
from src.database.db_sqlite import get_account_info


# 登录请求标准化参数模型
class LoginBody(BaseModel):
    uid: str
    password: str

app = FastAPI(title="FeatherPen V1.0.0 Offline Backend")

# 静态前端资源挂载
PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEB_DIRECTORY = PROJECT_ROOT / "web"
if not WEB_DIRECTORY.exists():
    raise FileNotFoundError(f"前端资源目录不存在：{WEB_DIRECTORY}")
app.mount("/", StaticFiles(directory=str(WEB_DIRECTORY), html=True), name="frontend_static")

@app.get("/api/status")
async def get_service_status():
    """获取服务基础运行状态信息"""
    return {
        "service_name": "FeatherPen",
        "version": "V1.0.0",
        "offline_uid": config["security"]["offline_fixed_uid"]
    }

@app.post("/api/v1/user/login")
async def user_login(body: LoginBody):
    """
    统一离线登录业务接口
    三层账号校验逻辑：1.离线游客免密 2.内置特权账号 3.数据库初始化账号
    :param body: 前端提交uid、password参数
    :return: 标准化响应 {code, detail, data}
    """
    uid_input = body.uid.strip()
    pwd_input = body.password.strip()

    # 第一层：前后端统一账号密码格式校验
    format_check = verify_local_account(uid_input, pwd_input)
    if format_check["code"] != 200:
        return format_check

    # 分支1：离线游客账号 127001，空白密码直接放行
    if uid_input == OFFLINE_GUEST_UID:
        return {
            "code": 200,
            "detail": "离线游客登录成功",
            "data": {
                "uid": OFFLINE_GUEST_UID,
                "level": 0,
                "point": 999999999,
                "is_lv9": False
            }
        }

    # 分支2：内置6位特权账号，匹配member_config配置
    if uid_input in PRIVILEGE_UID_LIST:
        member_cfg = _get_member_config()
        for item in member_cfg.default_member_list:
            if item["uid"] == uid_input and item["pwd"] == pwd_input:
                return {
                    "code": 200,
                    "detail": "特权账号登录成功",
                    "data": {
                        "uid": uid_input,
                        "level": item["level"],
                        "point": item["point"],
                        "is_lv9": item["level"] == 9
                    }
                }
        return {"code": 401, "detail": "特权账号密码错误"}

    # 分支3：读取sqlite数据库local_user表初始化账号
    db_user = get_account_info(uid_input)
    if not db_user:
        return {"code": 401, "detail": "账号不存在"}
    if db_user["password"] != pwd_input:
        return {"code": 401, "detail": "密码错误"}
    return {
        "code": 200,
        "detail": "登录成功",
        "data": {
            "uid": db_user["account"],
            "level": db_user["member_level"],
            "point": db_user["current_point"],
            "is_lv9": db_user["member_level"] == 9
        }
    }

def get_available_port(host: str, prefer_port: int) -> int:
    """检测端口占用，自动返回空闲端口"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, prefer_port))
        return prefer_port
    except OSError:
        with socket.socket(socket.AF_INET) as sock:
            sock.bind((host, 0))
            return sock.getsockname()[1]

def run_server():
    """后端服务启动入口，由main.py子线程调用"""
    host = config["network"]["bind_address"]
    prefer_port = config["network"]["preferred_port"]
    real_port = get_available_port(host, prefer_port)
    print("==== FeatherPen Web服务启动 ====")
    print(f"本地访问地址：http://{host}:{real_port}")
    print(f"离线游客固定UID：{config['security']['offline_fixed_uid']}")
    if real_port != prefer_port:
        print(f"警告：首选端口{prefer_port}占用，已自动切换至{real_port}")
    print("==============================")
    uvicorn.run(app, host=host, port=real_port, log_level="warning")

if __name__ == "__main__":
    """禁止单独运行本模块，统一启动入口为项目根main.py"""
    raise SystemExit("启动失败，请使用项目根目录main.py启动程序")
