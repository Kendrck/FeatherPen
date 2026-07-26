# FeatherPen/src/gui/web_window.py
"""
GB/T 8567 PyWebView桌面窗口标准化实现
基准文档：docs/API_MODULE_SPEC.md
核心流程：读取全局配置→轮询/api/v1/ping健康接口→加载本地web/index.html
约束：移除全部调试控件、调试输出，禁止直接访问HTTP空白页面逻辑
"""

import time
from pathlib import Path

import requests
import webview

from src.config.config_loader import load_global_config

global_config = load_global_config()
API_HOST = "127.0.0.1"
API_PORT = global_config.get("network", {}).get("preferred_port", 6554)
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"
WEB_INDEX_PATH = Path(__file__).parent.parent.parent / "web" / "index.html"
MAX_WAIT_SECONDS = 10


def wait_backend_service() -> bool:
    for _ in range(MAX_WAIT_SECONDS):
        try:
            resp = requests.get(f"{API_BASE_URL}/api/v1/ping", timeout=1)
            if resp.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    raise ConnectionError(f"后端{API_PORT}端口启动超时")


def create_standard_window() -> webview.Window:
    window = webview.create_window(
        title="FeatherPen 羽笔V1.0.0",
        url=str(WEB_INDEX_PATH),
        width=1200,
        height=800,
        resizable=True,
        private_mode=True,
    )
    return window


def start_gui() -> None:
    wait_backend_service()
    main_win = create_standard_window()
    webview.start(debug=False)
