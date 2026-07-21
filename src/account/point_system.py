"""
积分扣费逻辑、Lv9测试账号豁免控制
生成章节、角色整理、时间线、全文校验扣费统一入口
"""

from src.account.member_ctrl import check_lv9_skip_deduct
from src.config.config_loader import load_member_config

MEMBER_CFG = load_member_config()
POINT_COST = MEMBER_CFG["point_cost"]


def deduct_point(login_uid: str, type: str):
    """
    执行积分扣除，Lv9账号开关开启则跳过扣费
    :param login_uid: 当前登录用户UID
    :param type: 操作类型 gen_chapter/sort_role/gen_timeline/full_check
    """
    # Lv9账号豁免判断
    if check_lv9_skip_deduct(login_uid):
        return {"deduct_success": False, "tip": "Lv9特权账号积分豁免生效"}
    # 获取对应操作消耗积分
    cost = POINT_COST.get(type, 0)
    # 此处补充真实积分扣减数据库逻辑
    return {"deduct_success": True, "cost_point": cost}
