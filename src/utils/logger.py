#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一日志管理模块

提供全局统一的日志获取接口，支持控制台彩色输出与文件轮转记录。
所有模块必须通过此模块获取 Logger 实例，禁止直接使用 logging.getLogger()。
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 日志文件目录
LOG_DIR = Path(__file__).parent.parent.parent / "runtime" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 日志文件路径
LOG_FILE = LOG_DIR / "app.log"

# 日志格式
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 是否已初始化
_initialized = False


def init_log_system(max_bytes: int = 10 * 1024 * 1024, backup_count: int = 7) -> None:
    """
    初始化全局日志系统

    Args:
        max_bytes: 单个日志文件最大字节数，默认 10MB
        backup_count: 保留的历史日志文件数量，默认 7 个
    """
    global _initialized
    if _initialized:
        return

    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # 控制台处理器 (彩色输出)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)

    # 文件处理器 (轮转)
    file_handler = RotatingFileHandler(
        str(LOG_FILE), maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    _initialized = True
    root_logger.info("日志系统初始化完成")


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的 Logger 实例

    Args:
        name: 模块名称，通常传入 __name__

    Returns:
        配置好的 Logger 实例
    """
    if not _initialized:
        init_log_system()
    return logging.getLogger(name)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一日志管理模块

提供全局统一的日志获取接口，支持控制台彩色输出与文件轮转记录。
所有模块必须通过此模块获取 Logger 实例，禁止直接使用 logging.getLogger()。
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 日志文件目录
LOG_DIR = Path(__file__).parent.parent.parent / "runtime" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 日志文件路径
LOG_FILE = LOG_DIR / "app.log"

# 日志格式
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 是否已初始化
_initialized = False


def init_log_system(max_bytes: int = 10 * 1024 * 1024, backup_count: int = 7) -> None:
    """
    初始化全局日志系统

    Args:
        max_bytes: 单个日志文件最大字节数，默认 10MB
        backup_count: 保留的历史日志文件数量，默认 7 个
    """
    global _initialized
    if _initialized:
        return

    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # 控制台处理器 (彩色输出)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)

    # 文件处理器 (轮转)
    file_handler = RotatingFileHandler(
        str(LOG_FILE), maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    _initialized = True
    root_logger.info("日志系统初始化完成")


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的 Logger 实例

    Args:
        name: 模块名称，通常传入 __name__

    Returns:
        配置好的 Logger 实例
    """
    if not _initialized:
        init_log_system()
    return logging.getLogger(name)
