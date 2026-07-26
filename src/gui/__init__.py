# FeatherPen/src/gui/__init__.py
"""
GB/T 8567 GUI模块导出包
基准文档：docs/API_MODULE_SPEC.md
功能：对外统一暴露start_gui启动函数，供main.py调用
"""

from src.gui.web_window import start_gui

__all__ = ["start_gui"]
