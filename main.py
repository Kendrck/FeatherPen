#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FeatherPen 羽笔 V1.0.0 全局唯一启动入口

功能：
    负责项目环境初始化、全局配置加载、数据库初始化、
    监控调度启动、UI主程序调度、顶层异常捕获。

规范：
    全局唯一启动入口，禁止新增冗余业务逻辑，
    严格遵循跨平台离线优先架构。
"""

import os
import sys
import traceback

# [核心机制] 确保项目根目录在系统路径中，防止跨平台/打包后导入失败
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# --- 核心模块导入 ---
from src.ui.main_window import start_ui

from src.config.config_loader import load_global_config
from src.core.progress_monitor import init_monitor_scheduler
from src.database.db_sqlite import init_database
from src.utils.monitor.log_writer import init_log_system


def main():
    """主执行流程：按顺序初始化各子系统"""
    # 1. 初始化全局日志系统：自动创建分级日志目录、启用7天自动清理机制
    init_log_system()

    # 2. 加载全局核心配置：执行参数容错、URL合规校验、非法值自动回滚
    global_config = load_global_config()

    # 3. 初始化SQLite数据库：建立连接池与核心数据表结构
    init_database()

    # 4. 初始化后台调度器：AI进度监控与硬件资源监控双独立线程
    init_monitor_scheduler()

    # 5. 启动 PyQt6 可视化主界面：进入事件循环，联动后端所有业务服务
    start_ui(global_config)


if __name__ == "__main__":
    # [安全防线] 顶层全局异常捕获，保证启动报错可日志留存
    try:
        main()
    except Exception as e:
        # 使用 traceback 打印完整错误堆栈，便于定位具体崩溃行号
        error_msg = f"项目启动致命错误: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)

        # 尝试写入日志（如果日志系统已初始化）
        try:
            import logging

            logging.critical(error_msg)
        except Exception:
            pass

        sys.exit(1)
