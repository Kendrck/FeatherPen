"""
FeatherPen V1.0.0 全局配置管理模块
功能：统一加载YAML配置与环境变量，提供参数容错与自动回滚
规范：严格校验核心参数，非法值自动回滚默认值
"""
import os
import re
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class ConfigLoader:
    """
    配置加载器单例类
    负责解析config.yaml和环境变量，提供统一的配置访问接口
    """
    _instance = None
    _config = None

    def __new__(cls):
        """单例模式实现"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化配置加载器"""
        if ConfigLoader._config is None:
            self.config_path = Path("config.yaml")
            self._load_config()

    def _load_config(self) -> None:
        """加载并校验配置文件"""
        try:
            if not self.config_path.exists():
                logger.error(f"配置文件未找到: {self.config_path}")
                raise FileNotFoundError(f"配置文件未找到: {self.config_path}")

            with open(self.config_path, 'r', encoding='utf-8') as f:
                raw_config = yaml.safe_load(f)

            # 进行配置校验和修正
            self._validate_and_fix_config(raw_config)
            ConfigLoader._config = raw_config
            logger.info("配置文件加载并校验成功")

        except yaml.YAMLError as e:
            logger.error(f"配置文件YAML解析错误: {e}")
            raise
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise

    def _validate_and_fix_config(self, config: Dict) -> None:
        """
        校验并修正配置中的关键参数
        :param config: 配置字典引用
        """
        # 1. 校验监控参数 (1-999)
        monitor = config.get('monitor', {})
        ai_refresh = monitor.get('ai_monitor_refresh_sec', 1)
        if not isinstance(ai_refresh, int) or ai_refresh < 1 or ai_refresh > 999:
            logger.warning(f"ai_monitor_refresh_sec 值无效 ({ai_refresh})，回滚至默认值 1")
            monitor['ai_monitor_refresh_sec'] = 1

        hw_refresh = monitor.get('hardware_monitor_refresh_sec', 5)
        if not isinstance(hw_refresh, int) or hw_refresh < 1 or hw_refresh > 999:
            logger.warning(f"hardware_monitor_refresh_sec 值无效 ({hw_refresh})，回滚至默认值 5")
            monitor['hardware_monitor_refresh_sec'] = 5

        # 2. 校验本地API地址（强制规则）
        local_api = config.get('model_core', {}).get('local_api', {})
        base_url = local_api.get('base_url', '')
        if not self._is_valid_local_api_url(base_url):
            logger.error(f"本地API地址不合法: {base_url}")
            logger.error("唯一合法地址格式: http://127.0.0.1:1234/v1")
            # 自动修正为合法地址
            local_api['base_url'] = "http://127.0.0.1:1234/v1"
            logger.info("已将本地API地址重置为合法默认值")

        # 3. 校验路径配置
        paths = config.get('path', {})
        for key, value in paths.items():
            if value and not isinstance(value, str):
                logger.warning(f"路径配置 {key} 类型错误，已修正")
                paths[key] = str(value)

    def _is_valid_local_api_url(self, url: str) -> bool:
        """
        校验本地API地址是否合法
        :param url: 待校验URL
        :return: 合法返回True
        """
        if not url:
            return False
        # 唯一合法地址: http://127.0.0.1:1234/v1
        # 校验规则: 必须完全匹配，不允许空格、多余斜杠、缺失端口、缺失/v1后缀
        pattern = r'^http://127\.0\.0\.1:1234/v1$'
        return bool(re.match(pattern, url.strip()))

    def get(self, key: str, default: Any = None) -> Any:
        """
        通过点分路径获取配置值
        :param key: 配置键路径，如 'model_core.local_api.base_url'
        :param default: 默认值
        :return: 配置值
        """
        if ConfigLoader._config is None:
            return default

        keys = key.split('.')
        value = ConfigLoader._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_all(self) -> Dict:
        """获取完整配置字典"""
        return ConfigLoader._config

# 全局单例实例
config = ConfigLoader()
