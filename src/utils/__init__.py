# -*- coding: utf-8 -*-
"""
通用工具库模块初始化 V1.0.0
特性：无业务耦合，纯工具能力封装，全局通用
包含：硬件采集、日志管理、进度快照、国际化、语音工具
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块统一导出入口

提供日志系统和通用工具的快捷导入。
"""

from src.utils.logger import get_logger, init_log_system
from src.utils.monitor.log_writer import clean_old_logs

__all__ = ["get_logger", "init_log_system", "clean_old_logs"]
