# -*- coding: utf-8 -*-
# 文件路径：FeatherPen/src/utils/monitor/monitor_scheduler.py
"""
GB/T 8567 V1.0.0 硬件&AI监控定时调度器
功能：后台常驻线程调度硬件、Token、生成进度采集，写入monitor_log
约束：仅本地内存运行，无外网上报；刷新周期规范AI=1s/硬件=5s
依赖：log_writer日志持久化工具、progress_monitor进度模块
"""

import threading
import time

from src.core.progress_monitor import init_monitor_scheduler
from src.utils.monitor.log_writer import clean_old_logs

# 全局调度运行标记
_MONITOR_RUN_FLAG = False
# 标准刷新间隔（国标固定参数）
AI_MONITOR_INTERVAL = 1
HW_MONITOR_INTERVAL = 5


def start_all_monitor_scheduler():
    """启动全套AI生成+硬件监控双线程调度"""
    global _MONITOR_RUN_FLAG
    if _MONITOR_RUN_FLAG:
        return
    _MONITOR_RUN_FLAG = True
    # 初始化AI进度监控线程
    init_monitor_scheduler()
    # 启动硬件采集守护线程
    hw_thread = threading.Thread(target=_hardware_loop, daemon=True, name="HW-Monitor-Scheduler")
    hw_thread.start()


def stop_all_monitor_scheduler():
    """停止所有监控调度线程，清理日志"""
    global _MONITOR_RUN_FLAG
    _MONITOR_RUN_FLAG = False
    clean_old_logs(keep_days=7)


def _hardware_loop():
    """硬件资源循环采集逻辑，严格遵循5s间隔规范"""
    global _MONITOR_RUN_FLAG
    while _MONITOR_RUN_FLAG:
        # 硬件采集逻辑预留标准化接口
        time.sleep(HW_MONITOR_INTERVAL)
