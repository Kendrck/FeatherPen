# -*- coding: utf-8 -*-
"""
GB/T 8567 FastAPI后端服务入口
功能：注册全部离线业务接口，仅本地127.0.0.1访问，无外网接口
约束：废弃PyQt6相关代码，仅对接web前端页面
"""

from fastapi import FastAPI

from src.account.local_login import OFFLINE_GUEST_UID, verify_local_account
from src.config.config_loader import load_global_config
from src.database.db_sqlite import get_account_info, get_db_conn

app = FastAPI(title="FeatherPen V1.0.0 离线API", version="1.0.0")


@app.get("/")
def root_index():
    """服务根路由，返回运行状态"""
    return {"msg": "FeatherPen离线后端服务正常运行", "status": "running"}


@app.get("/api/v1/status")
def api_status():
    """页面初始化获取运行端口、程序版本、游客UID"""
    cfg = load_global_config()
    return {
        "code": 200,
        "detail": "服务运行正常",
        "data": {
            "service_name": "FeatherPen 离线服务",
            "version": "1.0.0",
            "offline_uid": OFFLINE_GUEST_UID,
            "web_port": cfg["network"]["preferred_port"],
        },
    }


@app.post("/api/v1/user/login")
def api_user_login(payload: dict):
    """本地账号登录接口，前后端二次正则校验，匹配数据库/游客/特权账号"""
    uid = payload.get("uid", "").strip() or OFFLINE_GUEST_UID
    pwd = payload.get("password", "").strip()

    validate_result = verify_local_account(uid, pwd)
    if validate_result["code"] != 200:
        return validate_result

    if uid == OFFLINE_GUEST_UID:
        return {
            "code": 200,
            "detail": "登录成功",
            "data": {
                "uid": uid,
                "level": 0,
                "current_point": 0,
                "is_lv": False,
            },
        }

    account = get_account_info(uid)
    if not account or account["password"] != pwd:
        return {"code": 401, "detail": "账号不存在或密码错误", "data": None}

    return {
        "code": 200,
        "detail": "登录成功",
        "data": {
            "uid": account["account"],
            "level": account["member_level"],
            "current_point": account["current_point"],
            "is_lv": account["member_level"] >= 1,
        },
    }


@app.get("/api/v1/user/check_name")
def api_check_username(username: str = ""):
    """账号查重接口，注册/登录前置唯一性校验"""
    username = username.strip()
    if not username:
        return {"code": 400, "detail": "username不能为空", "data": {"is_exist": False}}

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM local_user WHERE uid = ? OR bind_email = ?", (username, username))
    exist = cur.fetchone() is not None
    conn.close()
    return {
        "code": 200,
        "detail": "账号已占用" if exist else "账号可用",
        "data": {"is_exist": exist},
    }


@app.post("/api/v1/user/register")
def api_user_register(payload: dict):
    """本地新建普通账号，数据库唯一索引拦截重复邮箱、账号"""
    uid = payload.get("uid", "").strip()
    pwd = payload.get("password", "").strip()

    validate_result = verify_local_account(uid, pwd)
    if validate_result["code"] != 200:
        return validate_result

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM local_user WHERE uid = ? OR bind_email = ?", (uid, uid))
    if cur.fetchone() is not None:
        conn.close()
        return {"code": 400, "detail": "账号已存在", "data": None}

    bind_email = uid if "@" in uid else None
    cur.execute(
        "INSERT INTO local_user (uid, password, level, point, bind_email) VALUES (?, ?, ?, ?, ?)",
        (uid, pwd, 0, 999999999, bind_email),
    )
    conn.commit()
    conn.close()

    return {
        "code": 200,
        "detail": "注册成功",
        "data": {"uid": uid, "level": 0, "current_point": 999999999, "is_lv": False},
    }
