# -*- coding: utf-8 -*-
"""
GB/T 8567 本地账号登录校验模块
功能：实现国标账号/密码双层正则校验、数据库账号匹配
规范：账号6-20位，邮箱专用规则，密码≥6位；内置6位特权账号豁免校验
"""
import re

from src.database.db_sqlite import db_get_user_info
from src.utils.monitor.hardware_collect import get_mainboard_sn

# 全局统一正则（前后端完全同步）
USERNAME_PATTERN = r"^[a-zA-Z0-9_\-.]{6,20}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z]{2,}$"
PWD_PATTERN = r".{6,}"

def verify_local_account(uid: str, password: str) -> dict:
    """
    离线账号统一校验入口
    :param uid: 用户名/邮箱，空值触发主板SN自动登录，跳过正则
    :param password: 登录密码
    :return: 标准化返回体 code+detail/用户权限数据
    """
    # 空UID = 自动主板登录，跳过格式校验，兼容特权账号
    if not uid:
        auto_uid = get_mainboard_sn()[:6]
        user_data = db_get_user_info(auto_uid)
        if not user_data:
            return {"code":401, "detail":"自动登录无匹配账号"}
        if user_data["password"] != password:
            return {"code":401, "detail":"密码错误"}
        return {
            "code":200,
            "level": user_data["level"],
            "point": user_data["point"],
            "is_lv9": user_data["level"] ==9,
            "local_skip_point": False,
            "local_pressure": False,
            "cloud_sync_note":"云端同步V2.0开发"
        }
    # 非空账号：执行国标格式校验
    if "@" in uid:
        if not re.fullmatch(EMAIL_PATTERN, uid):
            return {"code":400, "detail":"邮箱格式非法，仅允许字母数字_-.@"}
    else:
        if not re.fullmatch(USERNAME_PATTERN, uid):
            return {"code":400, "detail":"账号错误：6-20位，仅字母数字_-.，禁止中文/空格特殊字符"}
    # 密码长度校验
    if not re.fullmatch(PWD_PATTERN, password):
        return {"code":400, "detail":"密码至少6位，推荐字母数字混合提升安全"}
    # 数据库匹配账号
    user_data = db_get_user_info(uid)
    if not user_data:
        return {"code":401, "detail":"账号不存在"}
    if user_data["password"] != password:
        return {"code":401, "detail":"登录密码错误"}
    # 校验通过，返回用户权限
    from src.config.config_loader import load_config
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
