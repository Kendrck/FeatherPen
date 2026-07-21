# -*- coding: utf-8 -*-
"""
全局配置加载与校验模块 V1.0.0
核心校验规则：
1. 监控参数仅支持1-999，非法值自动回滚默认
2. 本地API地址强制校验，非法地址重置官方标准地址
3. 统一参数容错与自动回滚机制，保障系统稳定运行
"""
import yaml
import os

# 官方唯一合法本地API地址（全局固定，不可修改）
DEFAULT_LOCAL_API_URL = "http://127.0.0.1:1234/v1"

def load_global_config():
    """
    加载并校验全局核心配置config.yaml
    :return: 合规校验后的全局配置字典
    """
    config_path = "config.yaml"
    # 读取原始配置文件
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # 监控参数区间容错校验
    monitor = config.get("monitor", {})
    if not 1 <= monitor.get("ai_monitor_refresh_sec", 1) <= 999:
        config["monitor"]["ai_monitor_refresh_sec"] = 1
    if not 1 <= monitor.get("hardware_monitor_refresh_sec", 5) <= 999:
        config["monitor"]["hardware_monitor_refresh_sec"] = 5
    
    # 本地API地址强制合规校验
    local_api_url = config["local_api"]["base_url"].strip()
    if local_api_url != DEFAULT_LOCAL_API_URL:
        config["local_api"]["base_url"] = DEFAULT_LOCAL_API_URL
    
    return config
