#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
账号业务服务模块
负责用户登录凭证校验、测试账号识别、Lv9特权判定、积分豁免控制业务逻辑。
业务规范基准文档：docs/API.md、docs/YESAPI_ACCOUNT.md
"""
from typing import Any, Dict, Optional

from src.utils.logger import get_logger

logger = get_logger(__name__)

# Lv9不朽特权账号白名单
LV9_PRIVILEGE_UIDS = {"99999999", "00000000"}
# 全量测试账号白名单
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
        """初始化账号服务，加载全局业务配置"""
        self._config = load_global_config()
        self._current_user: Optional[Dict[str, Any]] = None
        logger.info("AccountService 初始化完成")

    def verify_login(self, uid: str, password: str) -> Dict[str, Any]:
        """
        登录凭证校验，返回用户身份与权限信息

        Args:
            uid: 用户UID，8位数字字符串
            password: 用户明文密码，由上层调用方保证传输加密

        Returns:
            dict: 用户身份信息，包含token、等级、特权标记

        Raises:
            ValueError: UID格式不合法
            PermissionError: 账号密码校验失败
        """
        # UID格式合规校验
        if not uid or not isinstance(uid, str) or len(uid) != 8:
            raise ValueError("UID 必须为8位字符串")

        # 测试账号登录分支
        if uid in TEST_ACCOUNT_UIDS:
            if password != "administrator":
                raise PermissionError("测试账号密码错误，统一密码为administrator")

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

        # 正式账号云端登录接口预留
        raise PermissionError("正式账号登录接口尚未实现")

    def toggle_lv9_deduct(self, enable_skip: bool) -> bool:
        """
        切换Lv9特权账号积分扣费豁免开关

        Args:
            enable_skip: True=开启豁免（不扣费）；False=关闭豁免（正常扣费）

        Returns:
            bool: 切换完成后的开关状态

        Raises:
            PermissionError: 当前登录用户不具备Lv9不朽特权
        """
        if not self._current_user or not self._current_user.get("is_lv9_privilege"):
            raise PermissionError("仅Lv9不朽特权账号可操作积分豁免开关")

        self._current_user["current_deduct_switch"] = enable_skip
        logger.info(f"Lv9积分豁免开关切换完成，状态：{'开启' if enable_skip else '关闭'}")
        return enable_skip

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        获取当前登录用户信息

        Returns:
            Optional[Dict[str, Any]]: 用户信息字典；未登录返回None
        """
        return self._current_user

    def check_point_deduct(self) -> bool:
        """
        判断当前会话是否需要执行积分扣除

        Returns:
            bool: True=执行扣费；False=豁免扣费
        """
        if not self._current_user:
            return True

        if self._current_user.get("is_lv9_privilege") and self._current_user.get("current_deduct_switch", False):
            return False
        return True
