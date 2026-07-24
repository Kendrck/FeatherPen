"""
GB/T 8567-2006 国标业务注释
数据库模块初始化文件
功能：统一数据库模块导出、标准化模块调用入口、初始化数据库全局配置
约束：纯离线运行、无网络逻辑、零冗余代码
"""
__version__ = "1.0.0"
__author__ = "FeatherPen Dev"

# 导出核心数据库工具类与函数，统一项目调用规范
from .db_sqlite import (
    db_create_project,
    db_create_section,
    db_get_user_point,
    db_local_get_section_count,
    db_update_user_point,
    init_db,
)
from .monitor_db import clean_expired_monitor_log, insert_monitor_record
