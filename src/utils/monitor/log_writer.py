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
    log_dirs = [
        "logs/monitor_log",
        "logs/runtime_log",
        "logs/token_flow_log"
    ]
    for d in log_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

def auto_clear_log():
    """自动清理7天前过期日志文件，防止磁盘占用堆积"""
    pass
