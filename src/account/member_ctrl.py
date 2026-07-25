# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 会员权限与积分控制模块
文件路径: FeatherPen/src/account/member_ctrl.py
功能：读取会员配置、等级规则、Lv9积分豁免开关读写
约束：适配member_config.json根节点default_member_list，无废弃逻辑
"""
from __future__ import annotations

from typing import Any, Dict

from src.config.config_loader import load_member_config, save_member_privilege


def _get_member_config() -> Any:
    """加载全局会员配置单例"""
    return load_member_config()

def _get_level_rules() -> list[Dict[str, Any]]:
    """获取全部会员等级权限规则"""
    cfg = _get_member_config()
    return cfg.member_level

def get_member_level_rule(target_level: int) -> Dict[str, Any]:
    """根据等级获取对应权限配置，无匹配返回Lv0游客规则"""
    for rule in _get_level_rules():
        if rule["level"] == target_level:
            return rule
    return _get_level_rules()[0]

def check_lv9_skip_deduct(login_uid: str) -> bool:
    """校验当前账号是否开启积分豁免"""
    cfg = _get_member_config()
    lv9_list = cfg.cloud_privilege.get("lv9_uid_list", [])
    return login_uid in lv9_list and cfg.cloud_privilege["skip_point_deduct"]

def toggle_lv9_deduct_switch(enable_skip: bool) -> bool:
    """修改并持久化Lv9积分豁免全局开关"""
    cfg = _get_member_config()
    cfg.cloud_privilege["skip_point_deduct"] = enable_skip
    save_member_privilege({
        "cloud_privilege": cfg.cloud_privilege,
        "point_cost": cfg.point_cost,
        "member_level": cfg.member_level,
        "default_member_list": cfg.default_member_list
    })
    return True
