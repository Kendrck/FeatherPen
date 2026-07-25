# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 程序全局唯一启动入口
功能：初始化数据库、加载全局配置、子线程启动FastAPI、拉起PyWebView桌面窗口
约束：仅监听127.0.0.1，无外网开放逻辑，废弃PyQt6代码全移除
路径：FeatherPen/main.py
"""
import sys
import threading
from pathlib import Path


# ===================== 运行环境路径适配（源码/打包exe双兼容，解决打包闪退核心问题） =====================
def get_base_dir() -> Path:
    """
    获取程序根目录
    源码调试：返回脚本所在目录
    PyInstaller打包运行：返回exe所在目录
    """
    if hasattr(sys, "_MEIPASS"):
        # 打包运行模式
        return Path(sys.executable).resolve().parent
    else:
        # 源码开发模式
        return Path(__file__).resolve().parent

BASE_DIR = get_base_dir()
# =================================================================================================

import webview as pywebview

from src.config.config_loader import config
from src.database.init_db import init_database
from src.server.http_server import run_server


def start_api_service():
    """
    后台守护线程启动本地FastAPI服务
    作用：Web服务独立运行，不阻塞PyWebView桌面窗口主线程
    """
    run_server()


def main():
    """程序主启动逻辑"""
    # 1. 初始化SQLite数据表、兼容旧版本数据库结构
    init_database()

    # 2. 读取网络监听配置
    host = config["network"]["bind_address"]
    port = config["network"]["preferred_port"]
    target_url = f"http://{host}:{port}"

    # 3. 创建并启动FastAPI后台守护线程
    api_thread = threading.Thread(target=start_api_service, daemon=True)
    api_thread.start()

    # 4. 启动桌面Web窗口，连接本地后端服务
    pywebview.create_window(
        title="FeatherPen 羽笔 V1.0.0",
        url=target_url
    )
    pywebview.start()


if __name__ == "__main__":
    try:
        main()
    except Exception as exp:
        # 全局异常捕获，崩溃信息写入日志，解决exe一闪而过无法查看报错
        crash_log_path = BASE_DIR / "crash_error.log"
        import traceback
        crash_content = traceback.format_exc()
        with open(crash_log_path, "a", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write(crash_content)
            f.write("=" * 70 + "\n\n")
        raise exp
