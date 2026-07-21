#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt6 应用入口模块

负责初始化 Qt 应用实例，管理登录页与主窗口的生命周期。
"""

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from ui.login_page import LoginPage

from src.account.account_service import AccountService
from src.utils.logger import get_logger
from ui.member_panel import MemberPanel

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """主窗口容器"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FeatherPen 羽笔 V1.0.0")
        self.setMinimumSize(800, 600)

        # 使用堆叠布局管理页面切换
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 初始化页面
        self.login_page = LoginPage(self._on_login_success)
        self.member_panel = MemberPanel()

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.member_panel)

        # 默认显示登录页
        self.stack.setCurrentWidget(self.login_page)
        logger.info("主窗口初始化完成")

    def _on_login_success(self, user_info: dict):
        """登录成功回调，切换到会员面板"""
        logger.info(f"用户 {user_info['uid']} 登录成功，切换到主面板")
        self.member_panel.load_user(user_info)
        self.stack.setCurrentWidget(self.member_panel)


def start_ui(global_config):
    """
    启动 PyQt6 可视化主界面

    Args:
        global_config: 全局配置对象
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
