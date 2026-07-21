#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监控子模块统一导出入口

提供日志清理等监控功能的快捷导入。
"""

from src.utils.monitor.log_writer import clean_old_logs, init_log_system

__all__ = ["clean_old_logs", "init_log_system"]
