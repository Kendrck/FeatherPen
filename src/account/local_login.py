# -*- coding: utf-8 -*-
"""
GB/T 8567 离线账号双层校验模块
功能：前端JS+后端Python双层正则拦截，豁免账号跳过格式校验
约束：永久移除硬件读取、云端登录逻辑，仅本地SQLite校验
"""
import re

from src.database.db_sqlite import db_get_user_info

# 全局统一正则（前后端完全对齐，无差异）
USERNAME_PATTERN = r"^[a-zA-Z0-9_\-.]{6,20}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z]{2,}$"
PWD_PATTERN = r".{6,}"

# 豁免账号白名单（跳过通用格式校验）
OFFLINE_GUEST_UID = "127001"
PRIVILEGE_UIDS = {"000000","111111","222222","333333","444444","555555","666666","777777","888888","999999"}

def verify_local_account(uid: str, password: str) -> dict:
    """
    离线账号统一校验入口
    :param uid: 用户名/邮箱/离线游客标识
    :param password: 登录明文密码
    :return: 标准化返回体 code+detail/用户权限数据
    """
    # 豁免账号直接跳过正则校验
    if uid in PRIVILEGE_UIDS or uid == OFFLINE_GUEST_UID:
        pass
    else:
        # 区分邮箱/普通账号格式校验
        if "@" in uid:
            if not re.fullmatch(EMAIL_PATTERN, uid):
                return {"code": 400, "detail": "邮箱格式非法，仅允许字母数字_-.@"}
        else:
            if not re.fullmatch(USERNAME_PATTERN, uid):
                return {"code": 400, "detail": "账号错误：6-20位，仅字母数字_-.，禁止中文空格特殊字符"}
        # 密码长度强制校验
        if not re.fullmatch(PWD_PATTERN, password):
            return {"code": 400, "detail": "密码至少6位，推荐字母数字混合提升安全"}
    # 数据库匹配账号
    user_data = db_get_user_info(uid)
    if not user_data:
        return {"code": 401, "detail": "账号不存在"}
    if user_data["password"] != password:
        return {"code": 401, "detail": "登录密码错误"}
    # 读取全局配置返回权限
    from src.config.config_loader import load_config
    cfg = load_config()
    return {
        "code": 200,
        "level": user_data["level"],
        "point": user_data["point"],
        "is_lv9": user_data["level"] == 9,
        "local_skip_point": cfg["signin"]["lv9_skip_point_default"],
        "local_pressure": cfg["signin"]["lv9_pressure_default"],
        "cloud_sync_note": "云端账号同步功能V2.0开发规划"
    }
