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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全局配置加载模块

负责加载 config.yaml 和 member_config.json，提供统一的配置访问接口。
所有配置项均带有类型提示和默认值回滚机制。
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 配置文件路径
CONFIG_YAML_PATH = PROJECT_ROOT / "config.yaml"
MEMBER_CONFIG_PATH = PROJECT_ROOT / "member_config.json"


@dataclass
class AppConfig:
    """应用配置数据类"""

    run_mode: int
    soft_name: str
    soft_cn_name: str
    soft_version: str
    db_secret_key: str
    yesapi_app_key: str
    yesapi_app_secret: str
    test_account_enable: bool
    lv9_skip_point_default: bool
    daily_sign_point: int
    ad_reward_point: int


@dataclass
class MemberConfig:
    """会员配置数据类"""

    test_account_uid: List[Dict[str, Any]]
    cloud_privilege: Dict[str, Any]
    point_cost: Dict[str, int]
    member_level: List[Dict[str, Any]]


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全局配置加载模块

负责加载 config.yaml 和 member_config.json，提供统一的配置访问接口。
所有配置项均带有类型提示和默认值回滚机制。
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 配置文件路径
CONFIG_YAML_PATH = PROJECT_ROOT / "config.yaml"
MEMBER_CONFIG_PATH = PROJECT_ROOT / "member_config.json"


@dataclass
class AppConfig:
    """应用配置数据类"""

    run_mode: int
    soft_name: str
    soft_cn_name: str
    soft_version: str
    db_secret_key: str
    yesapi_app_key: str
    yesapi_app_secret: str
    test_account_enable: bool
    lv9_skip_point_default: bool
    daily_sign_point: int
    ad_reward_point: int


@dataclass
class MemberConfig:
    """会员配置数据类"""

    test_account_uid: List[Dict[str, Any]]
    cloud_privilege: Dict[str, Any]
    point_cost: Dict[str, int]
    member_level: List[Dict[str, Any]]


class ConfigLoader:
    """配置加载器单例"""

    _instance = None
    _app_config: AppConfig = None
    _member_config: MemberConfig = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_config(self) -> None:
        """加载所有配置文件"""
        self._load_yaml_config()
        self._load_member_config()

    def _load_yaml_config(self) -> None:
        """加载 config.yaml"""
        if not CONFIG_YAML_PATH.exists():
            raise FileNotFoundError(f"配置文件不存在: {CONFIG_YAML_PATH}")

        with open(CONFIG_YAML_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 提取 system 配置
        system = data.get("system", {})
        signin = data.get("signin", {})
        point = data.get("point", {})

        self._app_config = AppConfig(
            run_mode=system.get("run_mode", 0),
            soft_name=system.get("soft_name", "FeatherPen"),
            soft_cn_name=system.get("soft_cn_name", "羽笔"),
            soft_version=system.get("soft_version", "1.0.0"),
            db_secret_key=system.get("db_secret_key", ""),
            yesapi_app_key=system.get("yesapi_app_key", ""),
            yesapi_app_secret=system.get("yesapi_app_secret", ""),
            test_account_enable=signin.get("test_account_enable", True),
            lv9_skip_point_default=signin.get("lv9_skip_point_default", True),
            daily_sign_point=point.get("daily_sign_point", 100),
            ad_reward_point=point.get("ad_reward_point", 50),
        )

    def _load_member_config(self) -> None:
        """加载 member_config.json"""
        if not MEMBER_CONFIG_PATH.exists():
            raise FileNotFoundError(f"会员配置文件不存在: {MEMBER_CONFIG_PATH}")

        with open(MEMBER_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._member_config = MemberConfig(
            test_account_uid=data.get("test_account_uid", []),
            cloud_privilege=data.get("cloud_privilege", {}),
            point_cost=data.get("point_cost", {}),
            member_level=data.get("member_level", []),
        )

    @property
    def app(self) -> AppConfig:
        """获取应用配置"""
        if self._app_config is None:
            self.load_config()
        return self._app_config

    @property
    def member(self) -> MemberConfig:
        """获取会员配置"""
        if self._member_config is None:
            self.load_config()
        return self._member_config


# 全局配置实例
config = ConfigLoader()


def load_global_config() -> AppConfig:
    """快捷函数：加载全局应用配置"""
    return config.app


def load_member_config() -> MemberConfig:
    """快捷函数：加载会员配置"""
    return config.member
