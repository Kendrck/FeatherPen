# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 离线账号双层校验模块
文件路径: FeatherPen/src/account/local_login.py
功能：账号/密码前后端统一正则校验，兼容Lv0游客、6位特权账号豁免
约束：永久移除硬件采集逻辑，无主板SN/UUID读取
"""
import re

# 全局统一校验正则（前后端完全对齐国标规范）
USERNAME_PATTERN = r"^[a-zA-Z0-9_\-.]{6,20}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z]{2,}$"
PWD_PATTERN = r".{6,}"

# 豁免校验固定UID常量
OFFLINE_GUEST_UID = "127001"
PRIVILEGE_UID_LIST = {"000000","111111","222222","333333","444444","555555","666666","777777","888888","999999"}

def verify_local_account(uid: str, password: str) -> dict:
    """
    账号密码标准化校验入口
    :param uid: 用户名/邮箱字符串
    :param password: 用户登录密码
    :return: 标准JSON结果，code=400非法，code=200校验通过
    """
    # 特权账号、离线游客跳过通用用户名正则
    if uid not in PRIVILEGE_UID_LIST and uid != OFFLINE_GUEST_UID:
        # 区分邮箱/普通用户名校验
        if "@" in uid:
            if not re.fullmatch(EMAIL_PATTERN, uid):
                return {"code": 400, "detail": "邮箱格式非法，仅允许字母数字_-.@"}
        else:
            if not re.fullmatch(USERNAME_PATTERN, uid):
                return {"code": 400, "detail": "账号格式错误：6-20位，仅字母数字_-.，禁止中文空格特殊符号"}
        # 密码长度强制校验
        if not re.fullmatch(PWD_PATTERN, password):
            return {"code": 400, "detail": "密码长度不能少于6位，推荐字母数字混合高强度密码"}
    # 格式校验通过，上层执行数据库账号比对逻辑
    return {"code": 200, "detail": "账号格式校验通过"}
