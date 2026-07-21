# -*- coding: utf-8 -*-
"""
AI创作核心引擎模块初始化 V1.0.0
包含：模型适配、上下文管理、角色归档、小说生成、剧情校验、进度监控核心能力
"""
from .llm_api import model_request, check_model_loaded
from .memory_filter import filter_history_context
from .role_extract import extract_and_archive_role
from .novel_auto_gen import auto_generate_novel
from .world_check import check_world_consistency
from .progress_monitor import get_generate_progress

# 核心对外开放接口
__all__ = [
    "model_request", "check_model_loaded", "filter_history_context",
    "extract_and_archive_role", "auto_generate_novel", "check_world_consistency",
    "get_generate_progress"
]
