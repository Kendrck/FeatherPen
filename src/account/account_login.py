"""云端测试账号校验与登录逻辑。"""

from __future__ import annotations

from typing import Any, Dict

from src.account.member_ctrl import get_member_level_rule
from src.config.config_loader import load_member_config


def _get_member_config() -> Any:
    """获取会员配置对象。"""
    return load_member_config()


def match_test_account(input_uid: str, input_pwd: str) -> Dict[str, Any]:
    """校验输入 UID 与密码是否为白名单测试账号。"""
    member_config = _get_member_config()
    white_list = member_config.test_account_uid
    lv9_uid_list = member_config.cloud_privilege.get("lv9_uid_list", [])

    for item in white_list:
        if item.get("uid") == input_uid and item.get("pwd") == input_pwd:
            is_lv9 = input_uid in lv9_uid_list
            return {
                "match_success": True,
                "level": item.get("level", 0),
                "is_test_account": True,
                "is_lv9_privilege": is_lv9,
                "uid": input_uid,
                "point": item.get("point", 0),
            }

    return {
        "match_success": False,
        "level": 0,
        "is_test_account": False,
        "is_lv9_privilege": False,
    }


def cloud_login_handler(username: str, password: str, login_type: int) -> Dict[str, Any]:
    """登录接口核心业务处理。"""
    match_res = match_test_account(username, password)
    level_rule = get_member_level_rule(match_res["level"])
    member_config = _get_member_config()
    skip_deduct_switch = member_config.cloud_privilege.get("skip_point_deduct", False)

    return {
        "code": 200,
        "msg": "登录成功",
        "ext_info": level_rule,
        "is_test_account": match_res["is_test_account"],
        "is_lv9_privilege": match_res["is_lv9_privilege"],
        "current_deduct_switch": skip_deduct_switch,
    }
