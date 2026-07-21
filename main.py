#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FeatherPen 羽笔 V1.0.0 全局唯一启动入口
功能：负责项目环境初始化、全局配置加载、数据库初始化、监控调度启动、UI主程序调度、顶层异常捕获
规范：全局唯一启动入口，禁止新增冗余业务逻辑，严格遵循跨平台离线优先架构
"""
import sys
import os
from src.config.config_loader import load_global_config
from src.utils.monitor.log_writer import init_log_system
from src.database.db_sqlite import init_database
from src.ui.main_window import start_ui
from src.core.progress_monitor import init_monitor_scheduler

def main():
    # 初始化全局日志系统：自动创建分级日志目录、启用7天自动清理机制
    init_log_system()
    # 加载全局核心配置，执行参数容错、URL合规校验、非法值自动回滚
    global_config = load_global_config()
    # 初始化SQLite数据库连接池与核心数据表结构
    init_database()
    # 初始化AI进度监控、硬件资源监控双独立调度器
    init_monitor_scheduler()
    # 启动PyQt6可视化主界面，联动后端所有业务服务
    start_ui(global_config)

if __name__ == "__main__":
    # 顶层全局异常捕获，保证启动报错可日志留存
    try:
        main()
    except Exception as e:
        print(f"项目启动失败：{str(e)}")
        sys.exit(1)
