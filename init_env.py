#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FeatherPen V1.0.0 跨平台环境初始化脚本
功能：Python版本校验、项目必备目录自动创建、批量安装锁定依赖
适配：Windows / Linux / macOS / Android 全平台统一环境初始化
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """
    校验系统Python版本
    强制要求：Python3.14，版本不符直接终止初始化
    """
    version = sys.version_info
    if version.major != 3 or version.minor != 14:
        raise Exception(f"环境错误：当前Python版本{version.major}.{version.minor}，项目仅支持Python3.14")

def init_project_dir():
    """
    自动创建项目核心目录
    规避目录缺失导致的日志、数据、配置读写报错
    """
    dir_list = [
        "logs/monitor_log",
        "logs/runtime_log",
        "logs/token_flow_log",
        "Book/User",
        "docs"
    ]
    for dir_path in dir_list:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def install_dependencies():
    """
    批量安装项目锁定依赖
    基于requirements.txt统一安装，保障环境一致性
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    check_python_version()
    init_project_dir()
    install_dependencies()
    print("FeatherPen V1.0.0 跨平台环境初始化完成，环境适配正常")
