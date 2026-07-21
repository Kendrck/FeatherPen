#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 内容生成引擎

负责对接云端 API 或本地 GGUF 模型，执行小说内容生成任务。
生成前自动判定积分豁免状态，按规则执行扣费或跳过。
"""

from typing import Any, Dict, Optional

from src.account.account_service import AccountService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GenerateEngine:
    """AI 生成引擎核心类"""

    def __init__(self) -> None:
        """初始化生成引擎"""
        self._account_service = AccountService()
        self._api_base_url = "http://127.0.0.1:1234/v1"
        logger.info("GenerateEngine 初始化完成")

    def generate_content(
        self, prompt: str, volume: str, chapter: str, section: str
    ) -> Dict[str, Any]:
        """
        执行内容生成任务

        Args:
            prompt: 生成提示词
            volume: 卷编号
            chapter: 章编号
            section: 节编号

        Returns:
            包含生成内容和消耗积分的字典

        Raises:
            RuntimeError: 生成失败时抛出
        """
        logger.info(f"开始生成: 卷{volume} 章{chapter} 节{section}")

        # 1. 判定是否需要扣费
        need_deduct = self._account_service.check_point_deduct()
        points_cost = 0

        if need_deduct:
            points_cost = self._calculate_points(volume, chapter, section)
            logger.info(f"本次生成消耗积分: {points_cost}")
        else:
            logger.info("Lv9 积分豁免已开启，本次生成不消耗积分")

        # 2. 执行生成 (当前为模拟返回，后续对接真实 API)
        # TODO: 对接云端 API 或本地 GGUF 模型
        generated_text = self._call_model(prompt)

        return {
            "volume": volume,
            "chapter": chapter,
            "section": section,
            "content": generated_text,
            "points_cost": points_cost,
            "is_exempt": not need_deduct,
        }

    def _calculate_points(self, volume: str, chapter: str, section: str) -> int:
        """
        计算生成消耗的积分

        Args:
            volume: 卷编号
            chapter: 章编号
            section: 节编号

        Returns:
            消耗积分数
        """
        # 基础消耗: 每节 10 积分
        base_cost = 10
        # TODO: 根据卷/章层级动态调整消耗
        return base_cost

    def _call_model(self, prompt: str) -> str:
        """
        调用 AI 模型生成内容

        Args:
            prompt: 生成提示词

        Returns:
            生成的文本内容
        """
        # TODO: 实现真实的 API 调用或本地模型推理
        # 当前返回占位文本，确保链路可跑通
        return f"[AI生成内容占位] 提示词: {prompt[:50]}..."


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 内容生成引擎 (V2.0 真实对接版)

负责对接云端大模型 API 或本地 GGUF 模型，执行小说内容生成任务。
生成前自动判定积分豁免状态，按规则执行扣费并写入数据库流水。
"""

from typing import Any, Dict, Optional

import requests

from src.account.account_service import AccountService
from src.config.config_loader import load_global_config
from src.database.account_repo import AccountRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GenerateEngine:
    """AI 生成引擎核心类"""

    def __init__(self) -> None:
        """初始化生成引擎"""
        self._account_service = AccountService()
        self._account_repo = AccountRepository()
        self._config = load_global_config()

        # 默认本地 LM Studio / Ollama 地址
        self._api_base_url = "http://127.0.0.1:1234/v1"
        self._model_name = "local-gguf-model"

        logger.info("GenerateEngine V2.0 初始化完成")

    def generate_content(
        self, prompt: str, volume: str, chapter: str, section: str
    ) -> Dict[str, Any]:
        """
        执行内容生成任务

        Args:
            prompt: 生成提示词
            volume: 卷编号
            chapter: 章编号
            section: 节编号

        Returns:
            包含生成内容和消耗积分的字典

        Raises:
            RuntimeError: 生成失败时抛出
        """
        logger.info(f"开始生成: 卷{volume} 章{chapter} 节{section}")

        # 1. 判定是否需要扣费
        need_deduct = self._account_service.check_point_deduct()
        points_cost = 0

        if need_deduct:
            points_cost = self._config.app.generate_cost_per_section
            logger.info(f"本次生成消耗积分: {points_cost}")
        else:
            logger.info("Lv9 积分豁免已开启，本次生成不消耗积分")

        # 2. 执行生成
        try:
            generated_text = self._call_model(prompt)
        except Exception as e:
            logger.error(f"AI 生成失败: {e}")
            raise RuntimeError(f"AI 模型调用异常: {str(e)}")

        # 3. 执行扣费并写入流水
        if need_deduct and points_cost > 0:
            self._deduct_points(points_cost)

        return {
            "volume": volume,
            "chapter": chapter,
            "section": section,
            "content": generated_text,
            "points_cost": points_cost,
            "is_exempt": not need_deduct,
        }

    def _call_model(self, prompt: str) -> str:
        """
        调用 AI 模型生成内容 (OpenAI 兼容协议)

        Args:
            prompt: 生成提示词

        Returns:
            生成的文本内容
        """
        url = f"{self._api_base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self._model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位专业的网络小说作家，请根据提示词续写内容。",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
            "max_tokens": 2048,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        logger.info(f"AI 生成成功，返回字数: {len(content)}")
        return content

    def _deduct_points(self, amount: int) -> None:
        """
        扣除积分并写入流水

        Args:
            amount: 扣除积分数
        """
        current_user = self._account_service.get_current_user()
        if not current_user:
            logger.warning("未登录状态下尝试扣费，已跳过")
            return

        # TODO: 调用积分服务扣减余额
        logger.info(f"用户 {current_user['uid']} 扣除积分: {amount}")

        # 写入流水表 (这里假设 account_id 为当前用户的内部 ID)
        # 实际开发中应从 user 信息中获取内部 ID
        # self._account_repo.add_points_log(account_id=1, change_amount=-amount, type="generate")


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 内容生成引擎 (V2.0 真实对接版)

负责对接云端大模型 API 或本地 GGUF 模型，执行小说内容生成任务。
生成前自动判定积分豁免状态，按规则执行扣费并写入数据库流水。
"""

from typing import Any, Dict

import requests

from src.account.account_service import AccountService
from src.config.config_loader import load_global_config
from src.database.points_repo import PointsRepository
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GenerateEngine:
    """AI 生成引擎核心类"""

    def __init__(self) -> None:
        """初始化生成引擎"""
        self._account_service = AccountService()
        self._points_repo = PointsRepository()
        self._config = load_global_config()

        # 默认本地 LM Studio / Ollama 地址
        self._api_base_url = "http://127.0.0.1:1234/v1"
        self._model_name = "local-gguf-model"

        logger.info("GenerateEngine V2.0 初始化完成")

    def generate_content(
        self, prompt: str, volume: str, chapter: str, section: str, account_id: int
    ) -> Dict[str, Any]:
        """
        执行内容生成任务

        Args:
            prompt: 生成提示词
            volume: 卷编号
            chapter: 章编号
            section: 节编号
            account_id: 当前用户的数据库内部 ID (用于写入流水)

        Returns:
            包含生成内容和消耗积分的字典

        Raises:
            RuntimeError: 生成失败时抛出
        """
        logger.info(f"开始生成: 卷{volume} 章{chapter} 节{section}")

        # 1. 判定是否需要扣费
        need_deduct = self._account_service.check_point_deduct()
        points_cost = 0

        if need_deduct:
            points_cost = self._config.app.generate_cost_per_section
            logger.info(f"本次生成消耗积分: {points_cost}")
        else:
            logger.info("Lv9 积分豁免已开启，本次生成不消耗积分")

        # 2. 执行生成
        try:
            generated_text = self._call_model(prompt)
        except Exception as e:
            logger.error(f"AI 生成失败: {e}")
            raise RuntimeError(f"AI 模型调用异常: {str(e)}")

        # 3. 执行扣费并写入流水
        if need_deduct and points_cost > 0:
            self._points_repo.add_points_log(
                account_id=account_id, change_amount=-points_cost, log_type="generate"
            )

        return {
            "volume": volume,
            "chapter": chapter,
            "section": section,
            "content": generated_text,
            "points_cost": points_cost,
            "is_exempt": not need_deduct,
        }

    def _call_model(self, prompt: str) -> str:
        """
        调用 AI 模型生成内容 (OpenAI 兼容协议)

        Args:
            prompt: 生成提示词

        Returns:
            生成的文本内容
        """
        url = f"{self._api_base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self._model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位专业的网络小说作家，请根据提示词续写内容。",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.8,
            "max_tokens": 2048,
        }

        response = requests.post(url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        logger.info(f"AI 生成成功，返回字数: {len(content)}")
        return content
