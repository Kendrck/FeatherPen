"""
全局配置加载模块
实现多层配置合并策略：内置默认配置 < yaml文件 < 环境变量
"""
import os
from typing import Any, Dict

import yaml

# 内置默认基础配置
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
        "offline_user_id": "127001",
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
        "offline_data_dir": "./data/offline_127001",
        "cache_dir": "./cache",
        "log_dir": "./logs",
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
    """递归合并字典，子字典深度覆盖，基础值直接替换"""
    for k, v in override.items():
        if isinstance(v, dict) and k in base and isinstance(base[k], dict):
            merge_dict(base[k], v)
        else:
            base[k] = v
    return base

def load_config() -> Dict[str, Any]:
    """加载完整配置，逐层覆盖"""
    cfg = DEFAULT_CONFIG.copy()
    # 加载yaml配置
    if os.path.exists("config.yaml"):
        try:
            with open("config.yaml", "r", encoding="utf-8") as f:
                yaml_cfg = yaml.safe_load(f) or {}
                merge_dict(cfg, yaml_cfg)
        except Exception:
            pass

    # 环境变量覆盖
    env_bind = os.getenv("FP_NETWORK_BIND_ADDRESS")
    if env_bind:
        cfg["network"]["bind_address"] = env_bind

    env_port = os.getenv("FP_NETWORK_PREFERRED_PORT")
    if env_port and env_port.isdigit():
        cfg["network"]["preferred_port"] = int(env_port)

    env_uid = os.getenv("FP_SECURITY_OFFLINE_USER_ID")
    if env_uid:
        cfg["security"]["offline_user_id"] = env_uid

    return cfg

# 全局单例配置
config = load_config()
