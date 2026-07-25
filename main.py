# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 程序全局唯一启动入口
文件路径: FeatherPen/main.py
功能：初始化数据库、加载全局配置、后台启动FastAPI、拉起PyWebView桌面窗口
约束：仅本地127.0.0.1监听，移除PyQt6/Electron废弃逻辑，双兼容源码/打包运行
"""
import sys
import threading
from pathlib import Path

import webview as pywebview

# 先加载配置函数，再实例化配置对象
from src.config.config_loader import load_global_config

config = load_global_config()

def get_base_dir() -> Path:
    """
    获取程序根目录，双兼容源码运行 / PyInstaller打包exe
    源码：返回脚本所在目录；打包：返回exe所在目录
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent

BASE_DIR = get_base_dir()

# 业务模块导入
from src.database.init_db import init_database
from src.server.http_server import run_server


def start_api_service():
    """后台守护线程启动本地FastAPI离线服务，不阻塞桌面窗口主线程"""
    run_server()

def main():
    """程序主启动流程，严格遵循国标初始化顺序"""
    # 1. 初始化SQLite数据表，兼容旧版本数据库结构
    init_database()
    # 2. 读取网络绑定地址与端口
    host = config["network"]["bind_address"]
    port = config["network"]["preferred_port"]
    target_url = f"http://{host}:{port}"
    # 3. 启动API后台线程（守护线程，窗口关闭自动销毁）
    api_thread = threading.Thread(target=start_api_service, daemon=True)
    api_thread.start()
    # 4. 创建本地桌面Web窗口
    pywebview.create_window(title="FeatherPen 羽笔 V1.0.0", url=target_url)
    pywebview.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as exp:
        # 全局崩溃日志持久化，解决exe闪退无报错问题
        crash_log_path = BASE_DIR / "crash_error.log"
        import traceback
        crash_content = "=" * 70 + "\n" + traceback.format_exc() + "=" * 70 + "\n\n"
        with open(crash_log_path, "a", encoding="utf-8") as f:
            f.write(crash_content)
        raise exp
