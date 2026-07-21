"""
登录窗口UI页面
约束：不新增独立测试登录弹窗，10个快捷填充按钮内置表单下方
多语言文案统一读取assets/lib，禁止硬编码文字
"""

import json
from pathlib import Path

from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget

# 多语言文件路径
LANG_PATH = Path(__file__).parent.parent / "assets/lib/zh-CN.json"
# 白名单测试账号静态列表
WHITE_LIST = [
    {"level": 1, "uid": "11111111", "pwd": "administrator"},
    {"level": 2, "uid": "22222222", "pwd": "administrator"},
    {"level": 3, "uid": "33333333", "pwd": "administrator"},
    {"level": 4, "uid": "44444444", "pwd": "administrator"},
    {"level": 5, "uid": "55555555", "pwd": "administrator"},
    {"level": 6, "uid": "66666666", "pwd": "administrator"},
    {"level": 7, "uid": "77777777", "pwd": "administrator"},
    {"level": 8, "uid": "88888888", "pwd": "administrator"},
    {"level": 9, "uid": "99999999", "pwd": "administrator"},
    {"level": 9, "uid": "00000000", "pwd": "administrator"},
]


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 加载多语言文案
        with open(LANG_PATH, "r", encoding="utf-8") as f:
            self.lang = json.load(f)["login"]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.lang["cloud_title"])
        layout_main = QVBoxLayout()

        # 账号密码输入框
        self.uid_input = QLineEdit()
        self.uid_input.setPlaceholderText(self.lang["uid_input"])
        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText(self.lang["pwd_input"])

        # 10个测试账号快捷按钮容器
        btn_layout = QHBoxLayout()
        for item in WHITE_LIST:
            btn = QPushButton(f"Lv{item['level']} {item['uid']}")
            btn.setToolTip(self.lang["white_btn_tip"])
            # 点击自动填充UID和默认密码
            btn.clicked.connect(
                lambda checked, u=item["uid"], p=item["pwd"]: self.fill_account(u, p)
            )
            btn_layout.addWidget(btn)

        layout_main.addWidget(self.uid_input)
        layout_main.addWidget(self.pwd_input)
        layout_main.addLayout(btn_layout)
        self.setLayout(layout_main)

    def fill_account(self, uid: str, pwd: str):
        """快捷按钮填充账号密码"""
        self.uid_input.setText(uid)
        self.pwd_input.setText(pwd)
