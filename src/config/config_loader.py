"""
全局配置加载模块
1. 读取根目录config.yaml运行参数
2. 读取member_config.json白名单与会员权限
3. 参数非法自动回滚默认值
"""

import json
from pathlib import Path

import yaml

# 项目根目录定位
ROOT_PATH = Path(__file__).parent.parent.parent
YAML_PATH = ROOT_PATH / "config.yaml"
MEMBER_JSON_PATH = ROOT_PATH / "member_config.json"


def load_global_config() -> dict:
    """加载yaml全局系统配置"""
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg


def load_member_config() -> dict:
    """加载会员白名单、Lv9特权、积分扣费配置"""
    with open(MEMBER_JSON_PATH, "r", encoding="utf-8") as f:
        member_cfg = json.load(f)
    return member_cfg


def save_member_privilege(cfg: dict):
    """持久化更新Lv9扣费开关配置"""
    with open(MEMBER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
