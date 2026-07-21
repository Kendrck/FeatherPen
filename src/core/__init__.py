# -*- coding: utf-8 -*-
"""
AI创作核心引擎模块初始化 V1.0.0
包含：模型适配、上下文管理、角色归档、小说生成、剧情校验、进度监控核心能力
"""

from .llm_api import check_model_loaded, model_request
from .memory_filter import filter_history_context
from .novel_auto_gen import auto_generate_novel
from .progress_monitor import get_generate_progress
from .role_extract import extract_and_archive_role
from .world_check import check_world_consistency

# 核心对外开放接口
__all__ = [
    "model_request",
    "check_model_loaded",
    "filter_history_context",
    "extract_and_archive_role",
    "auto_generate_novel",
    "check_world_consistency",
    "get_generate_progress",
]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心模块统一导出入口

提供 AI 生成引擎等核心组件的快捷导入。
"""

from src.core.generate_engine import GenerateEngine

__all__ = ["GenerateEngine"]
