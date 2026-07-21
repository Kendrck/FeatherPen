"""
云端测试账号校验、登录逻辑模块
接口：/api/v1/account/cloud_login
职责：匹配白名单UID、下发测试账号标识、区分Lv9特权账号
"""

from src.account.member_ctrl import get_member_level_rule
from src.config.config_loader import load_member_config

# 全局缓存会员配置
MEMBER_CFG = load_member_config()
WHITE_LIST = MEMBER_CFG["test_account_uid"]
LV9_UID_LIST = MEMBER_CFG["cloud_privilege"]["lv9_uid_list"]


def match_test_account(input_uid: str, input_pwd: str) -> dict:
    """
    校验输入UID+密码是否为白名单测试账号
    :param input_uid: 用户输入8位UID
    :param input_pwd: 用户输入登录密码
    :return: 匹配结果、会员等级、特权标识
    """
    for item in WHITE_LIST:
        if item["uid"] == input_uid and item["pwd"] == input_pwd:
            is_lv9 = input_uid in LV9_UID_LIST
            return {
                "match_success": True,
                "level": item["level"],
                "is_test_account": True,
                "is_lv9_privilege": is_lv9,
                "uid": input_uid,
                "point": item["point"],
            }
    # 无匹配白名单账号
    return {
        "match_success": False,
        "level": 0,
        "is_test_account": False,
        "is_lv9_privilege": False,
    }


def cloud_login_handler(username: str, password: str, login_type: int) -> dict:
    """
    登录接口核心业务处理 /api/v1/account/cloud_login
    :param username: UID账号
    :param password: 明文密码（前端MD5加密后传输）
    :param login_type: 登录类型 0离线/1云端
    :return: 标准化返回体，携带权限标识
    """
    match_res = match_test_account(username, password)
    level_rule = get_member_level_rule(match_res["level"])
    skip_deduct_switch = MEMBER_CFG["cloud_privilege"]["skip_point_deduct"]

    return {
        "code": 200,
        "msg": "登录成功",
        "ext_info": level_rule,
        "is_test_account": match_res["is_test_account"],
        "is_lv9_privilege": match_res["is_lv9_privilege"],
        "current_deduct_switch": skip_deduct_switch,
    }
