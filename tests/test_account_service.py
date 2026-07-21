#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AccountService 单元测试

覆盖测试账号登录、Lv9 特权判定、积分豁免开关等核心场景，
确保业务逻辑与 docs/API.md 定义完全对齐。
"""

import pytest

from src.account.account_service import AccountService


@pytest.fixture
def account_service():
    """提供 AccountService 实例"""
    return AccountService()


def test_lv9_login_success(account_service):
    """验证 Lv9 测试账号登录成功"""
    result = account_service.verify_login("99999999", "administrator")
    assert result["uid"] == "99999999"
    assert result["level"] == 9
    assert result["is_lv9_privilege"] is True
    assert result["is_test_account"] is True


def test_normal_test_account_login(account_service):
    """验证普通测试账号 (Lv1-Lv8) 登录"""
    result = account_service.verify_login("33333333", "administrator")
    assert result["level"] == 3
    assert result["is_lv9_privilege"] is False


def test_wrong_password_raises_error(account_service):
    """验证测试账号密码错误时抛出异常"""
    with pytest.raises(PermissionError, match="测试账号密码错误"):
        account_service.verify_login("99999999", "wrong_password")


def test_invalid_uid_format(account_service):
    """验证非法 UID 格式抛出异常"""
    with pytest.raises(ValueError, match="UID 必须为8位字符串"):
        account_service.verify_login("123", "administrator")


def test_lv9_toggle_deduct(account_service):
    """验证 Lv9 积分豁免开关切换"""
    account_service.verify_login("99999999", "administrator")

    # 开启豁免
    state = account_service.toggle_lv9_deduct(True)
    assert state is True
    assert account_service.check_point_deduct() is False

    # 关闭豁免
    state = account_service.toggle_lv9_deduct(False)
    assert state is True
    assert account_service.check_point_deduct() is True


def test_non_lv9_cannot_toggle(account_service):
    """验证非 Lv9 账号无法操作积分豁免"""
    account_service.verify_login("33333333", "administrator")
    with pytest.raises(PermissionError, match="仅 Lv9 不朽特权账号"):
        account_service.toggle_lv9_deduct(True)
