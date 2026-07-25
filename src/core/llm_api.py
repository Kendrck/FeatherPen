# -*- coding: utf-8 -*-
"""轻量级 LLM 适配层。"""

from __future__ import annotations


class LLMUniversalClient:
    """提供一个最小可用的生成接口。"""

    def __init__(self) -> None:
        self._ready = True

    def check_service(self) -> bool:
        """静默服务状态检测。"""
        return self._ready

    def generate_text(self, user_prompt: str, system_prompt: str) -> str:
        """返回一个占位生成文本。"""
        return f"[AI生成内容占位] {user_prompt[:80]}"


llm_client = LLMUniversalClient()
