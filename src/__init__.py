"""
GB/T 8567-2006 国标业务注释
文件路径：FeatherPen/src/__init__.py
功能：Core 内核包导出入口，注册 FastAPI 离线接口
约束：V1.0 纯离线，无云端同步代码，仅本地 127.0.0.1 提供服务
"""
from fastapi import FastAPI

from src.account.local_login import verify_local_account
from src.utils.monitor.hardware_collect import get_mainboard_sn

app = FastAPI(title="FeatherPen V1.0.0 Offline API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "FeatherPen V1.0.0 离线服务已启动", "status": "running"}


@app.post("/api/v1/local/login")
def login_endpoint(payload: dict):
    """
    本地离线登录接口
    :param payload: {uid: str, password: str}
    :return: 账号权限信息
    """
    uid = payload.get("uid", "")
    password = payload.get("password", "")
    return verify_local_account(uid, password)


@app.get("/api/v1/hardware/sn")
def hardware_sn_endpoint():
    """
    读取本地主板硬件序列号接口
    注意：V1.0 仅本地返回，不上传云端
    """
    sn = get_mainboard_sn()
    return {"sn": sn}


@app.post("/api/v1/local/toggle_skip_point")
def toggle_skip_point(payload: dict):
    """
    Lv9 积分豁免开关接口
    """
    enable_skip = payload.get("enable_skip", False)
    return {"code": 200, "enable_skip": enable_skip, "message": "积分豁免配置已更新"}


@app.post("/api/v1/local/toggle_pressure")
def toggle_pressure(payload: dict):
    """
    Lv9 压测模式开关接口
    """
    enable_pressure = payload.get("enable_pressure", False)
    return {"code": 200, "enable_pressure": enable_pressure, "message": "压测模式配置已更新"}
