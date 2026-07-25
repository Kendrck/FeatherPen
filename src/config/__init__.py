# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 config模块导出入口
文件路径：FeatherPen/src/config/__init__.py
功能：统一向外暴露配置加载函数，禁止导出不存在的config变量
"""
from .config_loader import load_global_config, load_member_config, save_member_config

__all__ = [
    "load_global_config",
    "load_member_config",
    "save_member_config"
]
