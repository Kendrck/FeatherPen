"""
GB/T 8567-2006 国标业务注释
文件路径：FeatherPen/src/account/local_login.py
功能：本地离线账号登录校验逻辑
约束：无任何网络请求、云端校验代码
"""
import json

from src.config.config_loader import load_config
from src.database.db_sqlite import db_get_user_info

with open("src/account/member_config.json", "r", encoding="utf-8") as f:
    MEMBER_STATIC = json.load(f)


def verify_local_account(uid: str, password: str) -> dict:
    """
    本地账号登录校验入口
    :param uid: 6位数字离线账号
    :param password: 本地登录密码
    :return: 账号权限字典
    """
    if len(uid) != 6 or not uid.isdigit():
        return {"code": 400, "detail": "UID必须为6位纯数字"}

    user_data = db_get_user_info(uid)

    if not user_data:
        return {"code": 401, "detail": "账号不存在"}

    if user_data["password"] != password:
        return {"code": 401, "detail": "密码错误"}

    cfg = load_config()

    return {
        "code": 200,
        "level": user_data["level"],
        "point": user_data["point"],
        "is_lv9": user_data["level"] == 9,
        "local_skip_point": cfg["signin"]["lv9_skip_point_default"],
        "local_pressure": cfg["signin"]["lv9_pressure_default"],
        "cloud_sync_note": "云端同步功能规划至V2.0版本"
    }
