# -*- coding: utf-8 -*-
"""
src核心源码包初始化文件 V1.0.0
功能：统一导出项目核心业务模块，规范全局模块调用方式
规范：所有子模块统一注册，禁止零散导入
"""
# 导出全部核心业务模块
from . import account, config, core, database, utils

# 定义源码包版本，与项目版本统一
__version__ = "1.0.0"
