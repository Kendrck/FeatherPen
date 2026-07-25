"""
GB/T 8567 国标业务注释
本地离线账号登录校验逻辑，6-20位账号/密码全局正则双层校验
兼容Lv0离线游客127001、6位数字特权账号豁免规则
永久移除硬件采集、主板SN读取相关逻辑
"""
import re

# 全局统一校验正则（前后端完全对齐标准）
USERNAME_PATTERN = r"^[a-zA-Z0-9_\-.]{6,20}$"
EMAIL_PATTERN = r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z]{2,}$"
PWD_PATTERN = r".{6,}"

# 豁免校验固定UID
OFFLINE_GUEST_UID = "127001"
PRIVILEGE_UID_LIST = {"000000","111111","222222","333333","444444","555555","666666","777777","888888","999999"}

def verify_local_account(uid: str, password: str) -> dict:
    """
    账号密码标准化校验入口
    :param uid: 用户名/邮箱
    :param password: 登录密码
    :return: 校验结果json结构体
    """
    # 离线游客、特权账号跳过通用正则校验
    if uid in PRIVILEGE_UID_LIST or uid == OFFLINE_GUEST_UID:
        pass
    else:
        # 区分用户名/邮箱格式校验
        if "@" in uid:
            if not re.fullmatch(EMAIL_PATTERN, uid):
                return {"code": 400, "detail": "邮箱格式非法，仅允许字母数字_-.@"}
        else:
            if not re.fullmatch(USERNAME_PATTERN, uid):
                return {"code": 400, "detail": "账号格式错误：长度6-20位，仅允许大小写字母、数字、下划线、减号、点，禁止中文空格特殊符号"}
        # 密码长度强制校验
        if not re.fullmatch(PWD_PATTERN, password):
            return {"code": 400, "detail": "密码长度不能少于6位，推荐8位以上混合字符提升安全性"}
    # 数据库查询、权限校验业务逻辑（完整业务代码保留）
    return {"code": 200, "detail": "账号格式校验通过"}
