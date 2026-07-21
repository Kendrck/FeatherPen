# -*- coding: utf-8 -*-
"""
全局配置管理模块初始化 V1.0.0
功能：统一加载项目核心配置、参数容错、合规校验
"""
from .config_loader import load_global_config

__all__ = ["load_global_config"]
