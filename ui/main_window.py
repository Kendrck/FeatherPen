"""
会员面板UI
仅Lv9账号展示积分豁免开关，Lv0-Lv8隐藏该模块
切换下拉框实时调用toggle_lv9_deduct接口同步配置
"""

import json
from pathlib import Path

from PySide6.QtWidgets import QComboBox, QLabel, QVBoxLayout, QWidget

from src.account.member_ctrl import toggle_lv9_deduct_switch

LANG_PATH = Path(__file__).parent.parent / "assets/lib/zh-CN.json"


class MemberPanel(QWidget):
    def __init__(self, login_uid: str, is_lv9: bool):
        super().__init__()
        self.login_uid = login_uid
        self.is_lv9 = is_lv9
        # 加载会员多语言文案
        with open(LANG_PATH, "r", encoding="utf-8") as f:
            self.lang = json.load(f)["member"]
        self.init_panel()

    def init_panel(self):
        layout = QVBoxLayout()
        # 账号标签
        label_acc = QLabel(f"<font color='green'>{self.lang['white_label']}</font>")
        layout.addWidget(label_acc)
        if self.is_lv9:
            label_lv9 = QLabel(f"<font color='red'>{self.lang['lv9_label']}</font>")
            layout.addWidget(label_lv9)
            # Lv9积分豁免开关模块
            layout.addWidget(QLabel(self.lang["lv9_switch_title"]))
            self.switch_box = QComboBox()
            self.switch_box.addItems(["开启积分豁免", "关闭积分豁免"])
            self.switch_box.currentIndexChanged.connect(self.on_switch_change)
            self.tip_label = QLabel()
            layout.addWidget(self.switch_box)
            layout.addWidget(self.tip_label)
            self.refresh_tip()
        self.setLayout(layout)

    def on_switch_change(self, idx: int):
        """下拉框切换，同步后端开关配置"""
        enable_skip = idx == 0
        toggle_lv9_deduct_switch(enable_skip)
        self.refresh_tip()

    def refresh_tip(self):
        """刷新开关状态提示文字"""
        if self.switch_box.currentIndex() == 0:
            self.tip_label.setText(self.lang["switch_on_tip"])
        else:
            self.tip_label.setText(self.lang["switch_off_tip"])
