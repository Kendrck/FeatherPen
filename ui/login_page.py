#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
登录页面模块

提供用户登录界面，包含 UID/密码输入框和测试账号快捷按钮。
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.account.account_service import AccountService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(QWidget):
    """登录页面"""

    login_success = pyqtSignal(dict)

    def __init__(self, on_login_success):
        super().__init__()
        self._on_login_success = on_login_success
        self._account_service = AccountService()
        self._setup_ui()

    def _setup_ui(self):
        """构建登录界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # 标题
        title = QLabel("FeatherPen 羽笔 - 云端账号登录")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        # UID 输入
        self.uid_input = QLineEdit()
        self.uid_input.setPlaceholderText("8位账号UID")
        self.uid_input.setMaxLength(8)
        layout.addWidget(QLabel("账号 UID:"))
        layout.addWidget(self.uid_input)

        # 密码输入
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("登录密码")
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("登录密码:"))
        layout.addWidget(self.pwd_input)

        # 登录按钮
        login_btn = QPushButton("登 录")
        login_btn.setStyleSheet(
            "padding: 10px; font-size: 16px; background-color: #4CAF50; color: white;"
        )
        login_btn.clicked.connect(self._handle_login)
        layout.addWidget(login_btn)

        # 测试账号快捷按钮区
        test_group = QGroupBox("白名单测试账号 (快捷填充)")
        grid = QGridLayout()

        test_accounts = [
            ("Lv1", "11111111"),
            ("Lv2", "22222222"),
            ("Lv3", "33333333"),
            ("Lv4", "44444444"),
            ("Lv5", "55555555"),
            ("Lv6", "66666666"),
            ("Lv7", "77777777"),
            ("Lv8", "88888888"),
            ("Lv9", "99999999"),
            ("Lv9", "00000000"),
        ]

        for idx, (level, uid) in enumerate(test_accounts):
            btn = QPushButton(f"{level} {uid}")
            btn.clicked.connect(lambda checked, u=uid: self._fill_test_account(u))
            grid.addWidget(btn, idx // 5, idx % 5)

        test_group.setLayout(grid)
        layout.addWidget(test_group)

    def _fill_test_account(self, uid: str):
        """填充测试账号"""
        self.uid_input.setText(uid)
        self.pwd_input.setText("administrator")
        logger.debug(f"已填充测试账号: {uid}")

    def _handle_login(self):
        """处理登录逻辑"""
        uid = self.uid_input.text().strip()
        pwd = self.pwd_input.text().strip()

        try:
            user_info = self._account_service.verify_login(uid, pwd)
            self._on_login_success(user_info)
        except PermissionError as e:
            QMessageBox.warning(self, "登录失败", str(e))
        except ValueError as e:
            QMessageBox.warning(self, "输入错误", str(e))
        except Exception as e:
            QMessageBox.critical(self, "系统错误", f"登录异常: {str(e)}")
