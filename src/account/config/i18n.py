#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多语言管理模块

负责加载 assets/lib/ 下的语言包，提供统一的文本获取接口。
所有 UI 文案必须通过此模块获取，禁止硬编码。
"""

import json
from pathlib import Path
from typing import Any, Dict

# 语言包目录
LOCALE_DIR = Path(__file__).parent.parent.parent / "assets" / "lib"

# 支持的语言
SUPPORTED_LOCALES = ["zh-CN", "en-US"]

# 当前语言（默认中文）
CURRENT_LOCALE = "zh-CN"


class I18nManager:
    """多语言管理器单例"""

    _instance = None
    _translations: Dict[str, Dict[str, Any]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_all_locales()
        return cls._instance

    def _load_all_locales(self) -> None:
        """加载所有支持的语言包"""
        for locale in SUPPORTED_LOCALES:
            file_path = LOCALE_DIR / f"{locale}.json"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    self._translations[locale] = json.load(f)
            else:
                self._translations[locale] = {}

    def get_text(self, key: str, locale: str = None) -> str:
        """
        获取指定键的翻译文本

        Args:
            key: 翻译键，如 "login.cloud_title"
            locale: 语言代码，None 表示使用当前语言

        Returns:
            翻译后的文本，未找到时返回键本身
        """
        target_locale = locale or CURRENT_LOCALE
        keys = key.split(".")

        # 逐级查找
        data = self._translations.get(target_locale, {})
        for k in keys:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                return key  # 未找到返回原键

        return str(data)

    def set_locale(self, locale: str) -> None:
        """切换当前语言"""
        global CURRENT_LOCALE
        if locale in SUPPORTED_LOCALES:
            CURRENT_LOCALE = locale


# 全局实例
i18n = I18nManager()


def tr(key: str, locale: str = None) -> str:
    """快捷函数：获取翻译文本"""
    return i18n.get_text(key, locale)
