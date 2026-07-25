"""积分扣费逻辑与 Lv9 测试账号豁免控制。"""

from __future__ import annotations

from typing import Any, Dict

from src.account.member_ctrl import check_lv9_skip_deduct
from src.config.config_loader import load_member_config


def deduct_point(login_uid: str, type: str) -> Dict[str, Any]:
    """执行积分扣除，Lv9 账号开关开启则跳过扣费。"""
    member_config = load_member_config()
    point_cost = member_config.point_cost

    if check_lv9_skip_deduct(login_uid):
        return {"deduct_success": False, "tip": "Lv9特权账号积分豁免生效"}

    cost = point_cost.get(type, 0)
    return {"deduct_success": True, "cost_point": cost}
