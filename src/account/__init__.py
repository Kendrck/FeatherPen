# -*- coding: utf-8 -*-
"""
账号会员体系模块初始化文件 V1.0.0
包含：登录校验、账号状态管理、会员权限控制、积分扣费全业务逻辑
"""
from .account_login import check_login_status, user_logout
from .member_ctrl import get_user_level, check_permission
from .point_system import point_deduct, get_user_point

# 对外开放接口列表
__all__ = ["check_login_status", "user_logout", "get_user_level", "check_permission", "point_deduct", "get_user_point"]
