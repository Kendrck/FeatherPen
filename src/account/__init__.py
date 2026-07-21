# -*- coding: utf-8 -*-
"""
账号会员体系模块初始化文件 V1.0.0
包含：登录校验、账号状态管理、会员权限控制、积分扣费全业务逻辑
"""

from .account_login import check_login_status, user_logout
from .member_ctrl import check_permission, get_user_level
from .point_system import get_user_point, point_deduct

# 对外开放接口列表
__all__ = [
    "check_login_status",
    "user_logout",
    "get_user_level",
    "check_permission",
    "point_deduct",
    "get_user_point",
]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
账号模块统一导出入口

提供 AccountService 类的快捷导入，确保外部调用路径统一为:
    from src.account import AccountService
"""

from src.account.account_service import AccountService

__all__ = ["AccountService"]
