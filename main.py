# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 软件主启动入口
功能：异步启动FastAPI后端服务、初始化全项目环境、拉起PyWebView桌面客户端
约束：废弃PyQt6/Electron，仅本地127.0.0.1监听，无外网开放逻辑
"""
import threading

import uvicorn
import webview

from src.config.config_loader import load_config
from src.database.init_db import init_database


def start_fastapi_service():
    """后台异步启动本地离线API服务，仅监听本机8080端口"""
    uvicorn.run(
        app="src:app",
        host="127.0.0.1",
        port=8080,
        log_level="error"
    )

if __name__ == "__main__":
    # 1. 初始化SQLite本地数据库，创建标准业务数据表
    init_database()
    # 2. 加载全局离线配置
    global_config = load_config()
    # 3. 后台线程启动API服务，守护线程随主程序关闭
    api_thread = threading.Thread(target=start_fastapi_service, daemon=True)
    api_thread.start()
    # 4. 拉起本地Web桌面窗口，绑定前端首页
    webview.create_window(
        title="Feather 羽笔 V1.0.0 离线版",
        url="http://127.0.0.1:8080/index.html"
    )
    webview.start()
