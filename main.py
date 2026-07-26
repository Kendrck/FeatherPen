# -*- coding: utf-8 -*-
# FeatherPen/main.py
"""
GB/T 8567 程序顶层唯一启动入口
基准文档：STRUCTURE.md、API_MODULE_SPEC.md
执行顺序：路径兼容→数据库初始化→后台线程→等待ping→加载本地web首页
"""

import sys
import threading
from pathlib import Path


def get_base_dir() -> Path:
    """区分源码/打包exe根目录"""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


BASE_DIR = get_base_dir()

# 全部导入与文档登记名称完全一致
from src.config.config_loader import load_global_config
from src.database.init_db import init_database
from src.gui import start_gui
from src.server.http_server import run_server

config = load_global_config()


def start_api_service():
    """后台守护线程运行FastAPI服务"""
    run_server()


def main():
    # 初始化数据库表结构
    init_database()
    host = config["network"]["bind_address"]
    port = config["network"]["preferred_port"]
    # 启动后台API守护线程
    api_thread = threading.Thread(target=start_api_service, daemon=True)
    api_thread.start()
    # 轮询等待服务就绪再渲染窗口
    start_gui()


if __name__ == "__main__":
    try:
        main()
    except Exception as exp:
        # 仅留存崩溃日志，无调试打印
        crash_log_path = BASE_DIR / "crash_error.log"
        import traceback

        crash_content = "=" * 70 + "\n" + traceback.format_exc() + "=" * 70 + "\n\n"
        with open(crash_log_path, "a", encoding="utf-8") as f:
            f.write(crash_content)
        raise exp
