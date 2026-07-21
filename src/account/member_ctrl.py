"""
会员权限拦截、Lv9特权判定、扣费开关读取模块
"""

from src.config.config_loader import load_member_config

MEMBER_CFG = load_member_config()
LV9_UID_LIST = MEMBER_CFG["cloud_privilege"]["lv9_uid_list"]
PRIVILEGE_CFG = MEMBER_CFG["cloud_privilege"]
LEVEL_RULES = MEMBER_CFG["member_level"]


def get_member_level_rule(target_level: int) -> dict:
    """根据等级获取对应会员权限规则"""
    for rule in LEVEL_RULES:
        if rule["level"] == target_level:
            return rule
    # 默认返回Lv0离线游客权限
    return LEVEL_RULES[0]


def check_lv9_skip_deduct(login_uid: str) -> bool:
    """
    判断当前登录账号是否豁免积分扣费
    仅Lv9白名单账号受全局开关控制
    """
    if login_uid not in LV9_UID_LIST:
        return False
    return PRIVILEGE_CFG["skip_point_deduct"]


def toggle_lv9_deduct_switch(enable_skip: bool):
    """
    修改全局Lv9积分豁免开关，持久化保存配置
    接口：/api/v1/account/toggle_lv9_deduct
    """
    from src.config.config_loader import save_member_privilege

    MEMBER_CFG["cloud_privilege"]["skip_point_deduct"] = enable_skip
    save_member_privilege(MEMBER_CFG)
    return True
