"""会员权限与积分豁免控制。"""

from __future__ import annotations

from typing import Any, Dict

from src.config.config_loader import load_member_config, save_member_privilege


def _get_member_config() -> Any:
    """返回当前会员配置对象。"""
    return load_member_config()


def _get_level_rules() -> list[Dict[str, Any]]:
    """返回会员等级规则。"""
    member_config = _get_member_config()
    return member_config.member_level


def get_member_level_rule(target_level: int) -> Dict[str, Any]:
    """根据等级获取对应会员权限规则。"""
    for rule in _get_level_rules():
        if rule.get("level") == target_level:
            return rule
    return _get_level_rules()[0]


def check_lv9_skip_deduct(login_uid: str) -> bool:
    """判断当前登录账号是否豁免积分扣费。"""
    member_config = _get_member_config()
    lv9_uid_list = member_config.cloud_privilege.get("lv9_uid_list", [])
    if login_uid not in lv9_uid_list:
        return False
    return bool(member_config.cloud_privilege.get("skip_point_deduct", False))


def toggle_lv9_deduct_switch(enable_skip: bool) -> bool:
    """修改全局 Lv9 积分豁免开关并持久化。"""
    member_config = _get_member_config()
    member_config.cloud_privilege["skip_point_deduct"] = enable_skip
    save_member_privilege({
        "cloud_privilege": member_config.cloud_privilege,
        "point_cost": member_config.point_cost,
        "member_level": member_config.member_level,
        "default_member_list": member_config.test_account_uid,
    })
    return True
