# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 FastAPI 服务启动包
文件路径：FeatherPen/src/server/__init__.py
功能：对外暴露本地 FastAPI 服务入口 run_server
"""

from .http_server import run_server

__all__ = ["run_server"]
