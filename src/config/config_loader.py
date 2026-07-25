# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 全局配置加载模块
文件路径：FeatherPen/src/config/config_loader.py
功能：分层加载系统配置，优先级：内置默认配置 < config.yaml < 环境变量
约束：提供单一标准入口 load_config()，废弃所有别名；参数非法自动回落默认值
"""
import json
import os
from pathlib import Path
from typing import Any, Dict

import yaml

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_YAML = PROJECT_ROOT / "config.yaml"
MEMBER_JSON = PROJECT_ROOT / "member_config.json"
USER_CFG_PATH = PROJECT_ROOT / "data/Book/User/127001/user_setting.json"

# 底层内置默认配置（兜底基准）
DEFAULT_CONFIG: Dict[str, Any] = {
    "network": {
        "bind_address": "127.0.0.1",
        "preferred_port": 6554,
        "protocol": "tcp",
        "connect_timeout": 15,
        "read_timeout": 300,
        "write_timeout": 120,
        "max_concurrent_connections": 16,
        "thread_pool_size": 8,
        "enable_cors": True,
    },
    "security": {
        "offline_fixed_uid": "127001",
        "enable_cloud_auth": False,
        "api_key": "",
        "token_expire_hours": 24,
        "enable_ssl": False,
        "cert_file": "./certs/server.crt",
        "key_file": "./certs/server.key",
        "ip_whitelist": ["127.0.0.1"],
        "ip_blacklist": [],
        "log_mask_sensitive": True,
    },
    "storage": {
        "data_root": "./data",
        "offline_data_dir": "./data/Book/User/127001",
        "cache_dir": "./runtime/cache",
        "log_dir": "./runtime/logs",
        "log_max_size_mb": 50,
        "log_keep_days": 30,
        "export_dir": "./export",
    },
    "runtime": {
        "env_mode": "dev",
        "max_memory_mb": 2048,
        "pid_file": "./featherpen.pid",
        "run_as_service": False,
    },
    "generator": {
        "max_context_length": 8192,
        "default_temperature": 0.7,
    }
}


def merge_dict(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    递归深度合并字典配置
    :param base: 基础默认配置
    :param override: 外部覆盖配置
    :return: 合并后完整配置字典
    """
    for k, v in override.items():
        if isinstance(v, dict) and k in base and isinstance(base[k], dict):
            merge_dict(base[k], v)
        else:
            base[k] = v
    return base


def load_config() -> Dict[str, Any]:
    """
    【标准唯一入口】加载全局系统配置
    加载顺序：内置默认配置 → yaml文件 → 环境变量覆盖
    """
    cfg = DEFAULT_CONFIG.copy()
    # 加载yaml配置文件
    if CONFIG_YAML.exists():
        try:
            with open(CONFIG_YAML, "r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f) or {}
                merge_dict(cfg, yaml_data)
        except Exception:
            pass
    # 环境变量覆盖端口与离线UID
    env_port = os.getenv("FP_NETWORK_PREFERRED_PORT")
    if env_port and env_port.isdigit():
        cfg["network"]["preferred_port"] = int(env_port)
    env_uid = os.getenv("FP_SECURITY_OFFLINE_UID")
    if env_uid:
        cfg["security"]["offline_fixed_uid"] = env_uid
    return cfg


def load_member_config() -> Dict[str, Any]:
    """加载会员等级、积分权限配置"""
    if not MEMBER_JSON.exists():
        raise FileNotFoundError("缺失配置文件：member_config.json")
    with open(MEMBER_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_member_privilege(new_cfg: Dict[str, Any]) -> None:
    """持久化会员特权配置修改"""
    with open(MEMBER_JSON, "w", encoding="utf-8") as f:
        json.dump(new_cfg, ensure_ascii=False, indent=2)


def load_user_setting() -> Dict[str, Any]:
    """加载离线游客个性化配置，缺失返回默认模板"""
    default_user = {
        "signin": {"lv9_skip_point_default": False, "lv9_pressure_default": False},
        "database": {"db_path": "featherpen.db"},
        "crypto": {"aes_key": "FeatherPen2026OfflineKey"},
        "model": {"local_api": "http://127.0.0.1:1234/v1", "model_name": "qwen2.5-14b-instruct"}
    }
    if not USER_CFG_PATH.exists():
        return default_user
    try:
        with open(USER_CFG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_user


# 全局单例导出
config = load_config()
