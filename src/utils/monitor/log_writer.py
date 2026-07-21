# -*- coding: utf-8 -*-
"""
日志管理模块 V1.0.0
核心能力：日志目录初始化、分级日志写入、7天自动清理、日志生命周期管理
"""

import os
import time
from pathlib import Path


def init_log_system():
    """初始化全局日志目录结构，保障日志读写正常"""
    log_dirs = ["logs/monitor_log", "logs/runtime_log", "logs/token_flow_log"]
    for d in log_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def auto_clear_log():
    """自动清理7天前过期日志文件，防止磁盘占用堆积"""
    pass


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志监控与自动清理模块

负责日志文件的定期清理，按配置保留最近 N 天的日志记录。
由 main.py 启动时调用，确保运行时磁盘空间可控。
"""

import os
import time
from pathlib import Path

from src.utils.logger import get_logger

logger = get_logger(__name__)

# 日志目录
LOG_DIR = Path(__file__).parent.parent.parent / "runtime" / "logs"


def clean_old_logs(keep_days: int = 7) -> int:
    """
    清理超过指定天数的日志文件

    Args:
        keep_days: 保留天数，默认 7 天

    Returns:
        被删除的文件数量
    """
    if not LOG_DIR.exists():
        logger.warning(f"日志目录不存在: {LOG_DIR}")
        return 0

    cutoff_time = time.time() - (keep_days * 86400)
    deleted_count = 0

    for file_path in LOG_DIR.glob("*.log*"):
        if file_path.stat().st_mtime < cutoff_time:
            try:
                file_path.unlink()
                deleted_count += 1
                logger.debug(f"已清理过期日志: {file_path.name}")
            except OSError as e:
                logger.error(f"清理日志失败: {file_path.name}, 错误: {e}")

    logger.info(f"日志清理完成，共删除 {deleted_count} 个过期文件")
    return deleted_count


def init_log_system() -> None:
    """
    初始化日志系统并执行自动清理

    供 main.py 调用的统一入口，完成日志系统初始化和历史日志清理。
    """
    from src.utils.logger import init_log_system as _init_log

    _init_log()

    # 启动时自动清理过期日志
    clean_old_logs(keep_days=7)
