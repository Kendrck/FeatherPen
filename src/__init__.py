# -*- coding: utf-8 -*-
"""
GB/T 8567 FastAPI后端服务入口
功能：注册全部离线业务接口，仅本地127.0.0.1访问，无外网接口
约束：废弃PyQt6相关代码，仅对接web前端页面
"""
from fastapi import FastAPI

from src.account.local_login import verify_local_account
from src.utils.monitor.hardware_collect import get_mainboard_sn

app = FastAPI(title="FeatherPen V1.0.0 离线API", version="1.0.0")

@app.get("/")
def root_index():
    """服务根路由，返回运行状态"""
    return {"msg": "FeatherPen离线后端服务正常运行", "status": "running"}

@app.post("/api/v1/local/login")
def api_local_login(payload: dict):
    """本地账号登录接口，前后端双层账号密码校验"""
    uid = payload.get("uid", "").strip()
    pwd = payload.get("password", "").strip()
    return verify_local_account(uid, pwd)

@app.get("/api/v1/hardware/sn")
def api_get_mb_sn():
    """读取本机主板序列号（自动登录专用）"""
    return {"sn": get_mainboard_sn()}

@app.post("/api/v1/local/toggle_skip_point")
def api_toggle_skip(payload: dict):
    """Lv9积分豁免开关持久化接口"""
    from src.account.member_ctrl import toggle_lv9_deduct_switch
    enable = payload.get("enable_skip", False)
    toggle_lv9_deduct_switch(enable)
    return {"code":200, "enable_skip": enable, "msg":"积分豁免配置已保存"}

@app.post("/api/v1/local/toggle_pressure")
def api_toggle_pressure(payload: dict):
    """压力模式开关预留接口"""
    return {"code":200, "enable_pressure": payload.get("enable_pressure", False), "msg":"压力配置已更新"}

@app.get("/api/v1/user/check_name")
def api_check_username(payload: dict):
    """账号查重接口，注册/登录前置唯一性校验"""
    from src.database.db_sqlite import get_db_conn
    username = payload.get("username", "").strip()
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM local_user WHERE uid = ?", (username,))
    exist = cur.fetchone() is not None
    conn.close()
    return {"code":200, "is_exist": exist, "msg": "账号已占用" if exist else "账号可用"}
