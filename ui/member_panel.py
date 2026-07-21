# -*- coding: utf-8 -*-
"""
会员面板模块 V1.0.0
功能：可视化展示会员等级、积分余额、创作上限、专属权限说明、等级权益
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会员面板模块

展示当前登录用户的会员信息，Lv9 账号可操作积分豁免开关。
"""

from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.account.account_service import AccountService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MemberPanel(QWidget):
    """会员面板"""

    def __init__(self):
        super().__init__()
        self._account_service = AccountService()
        self._current_user = None
        self._setup_ui()

    def _setup_ui(self):
        """构建会员面板界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # 标题
        self.title_label = QLabel("会员面板")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # 用户信息
        self.user_info_label = QLabel("当前用户: 未登录")
        self.user_info_label.setStyleSheet("font-size: 16px; margin: 10px 0;")
        layout.addWidget(self.user_info_label)

        # Lv9 积分豁免开关 (默认隐藏)
        self.lv9_switch = QCheckBox("Lv9 不朽特权 - 积分豁免开关")
        self.lv9_switch.setStyleSheet("font-size: 14px; padding: 10px;")
        self.lv9_switch.setVisible(False)
        self.lv9_switch.toggled.connect(self._toggle_lv9_deduct)
        layout.addWidget(self.lv9_switch)

        # 状态提示
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.status_label)

        layout.addStretch()

    def load_user(self, user_info: dict):
        """加载用户信息到面板"""
        self._current_user = user_info

        # 更新用户信息显示
        level = user_info.get("level", 1)
        uid = user_info.get("uid", "unknown")
        self.user_info_label.setText(f"当前用户: {uid} (Lv{level})")

        # Lv9 账号显示积分豁免开关
        if user_info.get("is_lv9_privilege"):
            self.lv9_switch.setVisible(True)
            # 根据当前状态设置开关
            deduct_switch = user_info.get("current_deduct_switch", True)
            self.lv9_switch.setChecked(not deduct_switch)  # 勾选 = 开启豁免
            self._update_status_text(not deduct_switch)
        else:
            self.lv9_switch.setVisible(False)
            self.status_label.setText("普通账号，无积分豁免权限")

    def _toggle_lv9_deduct(self, checked: bool):
        """切换 Lv9 积分豁免"""
        try:
            # checked=True 表示开启豁免 (不扣费)
            enable_skip = checked
            self._account_service.toggle_lv9_deduct(enable_skip)
            self._update_status_text(enable_skip)
            logger.info(f"Lv9 积分豁免已{'开启' if enable_skip else '关闭'}")
        except PermissionError as e:
            QMessageBox.warning(self, "操作失败", str(e))
            # 恢复开关状态
            self.lv9_switch.blockSignals(True)
            self.lv9_switch.setChecked(not checked)
            self.lv9_switch.blockSignals(False)

    def _update_status_text(self, skip_enabled: bool):
        """更新状态提示文字"""
        if skip_enabled:
            self.status_label.setText("✅ 当前已开启积分豁免，生成、校正操作不消耗积分")
            self.status_label.setStyleSheet("color: #4CAF50; font-size: 12px;")
        else:
            self.status_label.setText("⚠️ 当前已关闭积分豁免，所有操作正常扣除积分")
            self.status_label.setStyleSheet("color: #FF9800; font-size: 12px;")
