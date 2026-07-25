# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 config模块导出控制
文件路径：FeatherPen/src/config/__init__.py
规范：统一对外暴露标准接口，废弃历史别名load_global_config
"""
from .config_loader import (
    config,
    load_config,
    load_member_config,
    load_user_setting,
    save_member_privilege,
)

# 标准对外导出清单
__all__ = [
    "load_config",
    "load_member_config",
    "save_member_privilege",
    "load_user_setting",
    "config"
]
