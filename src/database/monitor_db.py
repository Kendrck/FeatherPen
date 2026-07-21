# -*- coding: utf-8 -*-
"""
监控数据持久化模块 V1.0.0
功能：积分扣费流水记录、硬件监控数据、Token流量数据存储
"""
import time
from src.database.db_sqlite import db_insert

def add_point_log(opt_type: str, cost: int):
    """
    新增积分扣费流水日志
    :param opt_type: 扣费操作类型
    :param cost: 扣费积分数量
    """
    create_time = time.strftime("%Y-%m-%d %H:%M:%S")
    db_insert("INSERT INTO point_log (opt_type, cost, create_time) VALUES (?, ?, ?)", (opt_type, cost, create_time))

def save_monitor_data(gpu_usage: float, mem_usage: float, cpu_usage: float, token_flow: int):
    """
    保存硬件资源与Token流量监控数据
    :param gpu_usage: GPU显存占用率
    :param mem_usage: 内存占用率
    :param cpu_usage: CPU占用率
    :param token_flow: 实时Token流量
    """
    pass
