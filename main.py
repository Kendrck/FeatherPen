"""
FeatherPen V1.0.0 全局唯一启动入口
文档基准优先级：仓库目录 > 全平台兼容 > 初代开发规范
职责：初始化环境、加载配置、启动API服务、渲染主UI窗口
"""

import sys

from src.core.engine import init_ai_engine
from src.database.db_init import init_sqlite_db
from src.utils.multi_lang import init_language_pack
from ui.main_window import launch_main_ui

from src.account.account_login import init_account_service
from src.config.config_loader import load_global_config, load_member_config


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

"""
GB/T 8567-2006 国标业务注释
文件路径：FeatherPen/main.py
功能：程序全局唯一启动入口
1. 初始化 SQLite 数据库
2. 后台守护线程启动本地 FastAPI 服务
3. 初始化 PyWebView 桌面窗口
约束：V1.0 纯离线，无 Electron/PyQt6 逻辑
"""
import threading

import uvicorn
import webview

from src.config.config_loader import load_config
from src.database.init_db import init_database


def start_fastapi_service():
    """后台异步启动 FastAPI 本地服务，仅监听本地回环地址"""
    uvicorn.run(
        app="src:app",
        host="127.0.0.1",
        port=8080,
        log_level="error"
    )


if __name__ == "__main__":
    # 初始化数据库
    init_database()

    # 加载全局离线配置
    global_config = load_config()

    # 守护线程启动后端
    api_thread = threading.Thread(target=start_fastapi_service, daemon=True)
    api_thread.start()

    # 初始化桌面窗口
    webview.create_window(
        title="FeatherPen 羽笔 V1.0.0 离线版",
        url="http://127.0.0.1:8080/index.html"
    )
    webview.start()
