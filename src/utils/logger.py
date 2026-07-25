#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一日志管理模块。"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "runtime" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
_initialized = False


def init_log_system(max_bytes: int = 10 * 1024 * 1024, backup_count: int = 7) -> None:
    """初始化全局日志系统。"""
    global _initialized
    if _initialized:
        return

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    file_handler = RotatingFileHandler(
        str(LOG_FILE), maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    _initialized = True
    root_logger.info("日志系统初始化完成")


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的 Logger 实例。"""
    if not _initialized:
        init_log_system()
    return logging.getLogger(name)
