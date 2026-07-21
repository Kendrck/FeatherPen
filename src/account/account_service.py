#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
账号业务服务模块

负责处理用户登录校验、测试账号识别、Lv9 特权判定及积分豁免开关逻辑。
所有业务规则严格遵循 docs/API.md 与 docs/YESAPI_ACCOUNT.md 定义。
"""

from typing import Any, Dict, Optional

from src.config.config_loader import load_global_config
from src.utils.logger import get_logger

# 初始化模块日志
logger = get_logger(__name__)

# Lv9 不朽特权账号白名单 (严格匹配 docs/YESAPI_ACCOUNT.md)
LV9_PRIVILEGE_UIDS = {"99999999", "00000000"}

# 全量测试账号白名单 (Lv1-Lv9)
TEST_ACCOUNT_UIDS = {
    "11111111",
    "22222222",
    "33333333",
    "44444444",
    "55555555",
    "66666666",
    "77777777",
    "88888888",
    "99999999",
    "00000000",
}


class AccountService:
    """账号业务核心服务类"""

    def __init__(self) -> None:
        """初始化账号服务，加载全局配置"""
        self._config = load_global_config()
        self._current_user: Optional[Dict[str, Any]] = None
        logger.info("AccountService 初始化完成")

    def verify_login(self, uid: str, password: str) -> Dict[str, Any]:
        """
        校验登录凭证并返回用户扩展信息

        Args:
            uid: 用户 UID (8位数字字符串)
            password: 用户密码 (明文，由调用方负责加密传输)

        Returns:
            包含 token、等级、特权状态的字典，失败时抛出异常

        Raises:
            ValueError: UID 或密码格式错误
            PermissionError: 登录凭证校验失败
        """
        # 1. 基础格式校验
        if not uid or not isinstance(uid, str) or len(uid) != 8:
            raise ValueError("UID 必须为8位字符串")

        # 2. 测试账号快速通道 (仅校验密码)
        if uid in TEST_ACCOUNT_UIDS:
            if password != "administrator":
                raise PermissionError("测试账号密码错误，统一为 administrator")

            level = 9 if uid in LV9_PRIVILEGE_UIDS else int(uid[0])
            self._current_user = {
                "uid": uid,
                "level": level,
                "is_test_account": True,
                "is_lv9_privilege": uid in LV9_PRIVILEGE_UIDS,
                "token": f"test_token_{uid}",
            }
            logger.info(f"测试账号 {uid} (Lv{level}) 登录成功")
            return self._current_user

        # 3. 正式账号校验 (预留云端接口对接)
        # TODO: 对接 YesApi /api/v1/account/cloud_login
        raise PermissionError("正式账号登录接口尚未实现")

    def toggle_lv9_deduct(self, enable_skip: bool) -> bool:
        """
        切换 Lv9 积分豁免开关

        Args:
            enable_skip: True=开启豁免(不扣费), False=关闭豁免(正常扣费)

        Returns:
            切换后的实际状态

        Raises:
            PermissionError: 当前用户无 Lv9 特权
        """
        if not self._current_user or not self._current_user.get("is_lv9_privilege"):
            raise PermissionError("仅 Lv9 不朽特权账号可操作积分豁免开关")

        # 更新内存状态
        self._current_user["current_deduct_switch"] = enable_skip

        # TODO: 持久化到 config.yaml 或数据库
        logger.info(f"Lv9 积分豁免开关已切换为: {'开启' if enable_skip else '关闭'}")
        return enable_skip

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """获取当前登录用户信息，未登录返回 None"""
        return self._current_user

    def check_point_deduct(self) -> bool:
        """
        判定当前操作是否需要扣除积分

        Returns:
            True=需要扣费, False=豁免扣费
        """
        if not self._current_user:
            return True  # 未登录默认扣费

        # Lv9 且开启豁免 -> 不扣费
        if self._current_user.get("is_lv9_privilege") and self._current_user.get(
            "current_deduct_switch", False
        ):
            return False

        return True
