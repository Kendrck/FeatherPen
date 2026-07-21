"""
FeatherPen V1.0.0 全局唯一启动入口
文档基准优先级：仓库目录 > 全平台兼容 > 初代开发规范
职责：初始化环境、加载配置、启动API服务、渲染主UI窗口
"""

import sys

from src.core.engine import init_ai_engine
from src.database.db_init import init_sqlite_db
from src.utils.multi_lang import init_language_pack

from src.account.account_login import init_account_service
from src.config.config_loader import load_global_config, load_member_config
from ui.main_window import launch_main_ui


def main():
    # 1. 加载全局yaml配置
    global_cfg = load_global_config()
    # 2. 加载会员白名单json配置
    member_cfg = load_member_config()
    # 3. 初始化多语言文案包assets/lib
    init_language_pack()
    # 4. 初始化SQLite持久化数据库
    init_sqlite_db(global_cfg["system"]["db_secret_key"])
    # 5. 初始化账号登录、权限、积分扣费服务
    init_account_service(global_cfg, member_cfg)
    # 6. 初始化AI生成推理引擎（云端/本地/GGUF三模式）
    init_ai_engine(global_cfg)
    # 7. 启动主客户端UI
    launch_main_ui()


if __name__ == "__main__":
    main()

import sys

from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FeatherPen")
        self.resize(1200, 800)

        # 1. 设置对象名称 (非常重要！QSS 依赖这个来定位)
        self.setObjectName("main_window")

        # 2. 加载 QSS 文件
        style_file = QFile("ui/styles/main.qss")
        if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(style_file)
            self.setStyleSheet(stream.readAll())
            style_file.close()
        else:
            print("警告：无法加载 main.qss 样式表")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
