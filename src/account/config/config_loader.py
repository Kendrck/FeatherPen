# -*- coding: utf-8 -*-
"""
GB/T 8567 全局配置加载单例模块
功能：读取yaml系统配置、json会员配置，统一参数校验与默认兜底
约束：全局唯一ConfigLoader实例，禁止重复实例化
"""
import json
from dataclasses import dataclass
from pathlib import Path

import yaml

# 项目根路径常量
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_YAML = PROJECT_ROOT / "config.yaml"
MEMBER_JSON = PROJECT_ROOT / "member_config.json"

@dataclass
class AppConfig:
    """系统YAML配置数据类"""
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
    """会员JSON配置数据类"""
    test_account_uid: list[dict]
    cloud_privilege: dict
    point_cost: dict
    member_level: list[dict]

class ConfigLoader:
    _instance = None
    _app_config: AppConfig | None = None
    _member_config: MemberConfig | None = None

    def __new__(cls):
        """单例模式，全局仅生成一个配置实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_all(self):
        """一次性加载系统+会员全套配置"""
        self._load_yaml()
        self._load_member()

    def _load_yaml(self):
        """读取并校验config.yaml"""
        if not CONFIG_YAML.exists():
            raise FileNotFoundError("缺失全局配置文件 config.yaml")
        with open(CONFIG_YAML, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        sys_cfg = raw.get("system", {})
        sign_cfg = raw.get("signin", {})
        point_cfg = raw.get("point", {})
        self._app_config = AppConfig(
            run_mode=sys_cfg.get("run_mode", 0),
            soft_name=sys.get("soft_name", "FeatherPen"),
            soft_cn_name=sys_cfg.get("soft_cn_name", "羽笔"),
            soft_version=sys_cfg.get("soft_version", "V1.0.0"),
            db_secret_key=sys_cfg.get("db_secret_key", ""),
            yesapi_app_key=sys_cfg.get("yesapi_app_key", ""),
            yesapi_app_secret=sys_cfg.get("yesapi_app_secret", ""),
            test_account_enable=sign_cfg.get("test_account_enable", True),
            lv9_skip_point_default=sign_cfg.get("lv9_skip_point", False),
            daily_sign_point=point_cfg.get("daily_sign_point", 100),
            ad_reward_point=point_cfg.get("ad_reward_point", 5)
        )

    def _load_member(self):
        """读取member_config.json会员特权配置"""
        if not MEMBER_JSON.exists():
            raise FileNotFoundError("缺失会员配置 member_config.json")
        with open(MEMBER_JSON, "r", encoding="utf-8") as f:
            raw = json.load(f)
        self._member_config = MemberConfig(
            test_account_uid=raw.get("default_member_list", []),
            cloud_privilege=raw.get("cloud_privilege", {}),
            point_cost=raw.get("point_cost", {}),
            member_level=raw.get("member_level", [])
        )

    @property
    def app(self) -> AppConfig:
        """获取系统配置，未加载自动初始化"""
        if self._app_config is None:
            self.load_all()
        return self._app_config

    @property
    def member(self) -> MemberConfig:
        """获取会员权限配置"""
        if self._member_config is None:
            self.load_all()
        return self._member_config

# 全局单例导出
config = ConfigLoader()
def load_global_config() -> AppConfig:
    """对外快速获取系统配置"""
    return config.app
def load_member_config() -> MemberConfig:
    """对外快速获取会员配置"""
def save_member_privilege(new_cfg: dict):
    """持久化Lv9积分豁免开关至json文件"""
    with open(MEMBER_JSON, "w", encoding="utf-8") as f:
        json.dump(new_cfg, f, ensure_ascii=False, indent=2)
