# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 全局配置加载模块
文件路径：FeatherPen/src/config/config_loader.py
功能：统一加载config.yaml、member_config.json，解析网络/模型端口；提供环境变量覆盖、非法参数自动兜底逻辑
约束：无硬编码端口数字，所有端口从配置读取，绑定地址固定127.0.0.1
"""
import json
import os
from pathlib import Path

import yaml

# 项目根路径常量
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_YAML_PATH = PROJECT_ROOT / "config.yaml"
MEMBER_JSON_PATH = PROJECT_ROOT / "member_config.json"

def load_global_config() -> dict:
    """
    加载全局系统配置，包含网络端口、模型参数
    返回标准化配置字典，非法端口自动回落默认值
    """
    if not CONFIG_YAML_PATH.exists():
        return _get_default_config()

    with open(CONFIG_YAML_PATH, "r", encoding="utf-8") as f:
        raw_cfg = yaml.safe_load(f) or {}

    network = raw_cfg.get("network", {})
    llm = raw_cfg.get("llm", {})

    # 环境变量优先覆盖端口
    env_web_port = os.getenv("FP_NETWORK_PREFERRED_PORT")
    if env_web_port and env_web_port.isdigit():
        web_port = int(env_web_port)
    else:
        web_port = network.get("preferred_port", 6554)

    model_port = llm.get("local_api_port", 1234)

    # 端口合法性校验
    if not isinstance(web_port, int) or not (1024 <= web_port <= 65535):
        web_port = 6554
    if not isinstance(model_port, int) or not (1024 <= model_port <= 65535):
        model_port = 1234

    raw_cfg.setdefault("network", {})
    raw_cfg["network"]["bind_address"] = "127.0.0.1"
    raw_cfg["network"]["preferred_port"] = web_port

    raw_cfg.setdefault("llm", {})
    raw_cfg["llm"]["local_api_port"] = model_port

    return raw_cfg

def _get_default_config() -> dict:
    """缺失配置文件时返回国标默认端口模板"""
    return {
        "network": {
            "bind_address": "127.0.0.1",
            "preferred_port": 6554
        },
        "llm": {
            "local_api_port": 1234
        },
        "signin": {
            "lv9_skip_point_default": True,
            "lv9_pressure_default": False
        },
        "database": {
            "db_path": "featherpen.db"
        }
    }

def load_member_config() -> dict:
    """加载会员特权账号配置 member_config.json"""
    if not MEMBER_JSON_PATH.exists():
        return {"default_member_list": []}
    with open(MEMBER_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_member_config(cfg: dict):
    """持久化会员配置到 member_config.json"""
    with open(MEMBER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

# 对外导出列表
__all__ = [
    "load_global_config",
    "load_member_config",
    "save_member_config"
]
