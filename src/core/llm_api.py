"""
FeatherPen V1.0.0 多模型接口统一适配模块
功能：封装与云端API、本地API、本地GGUF模型的交互，提供统一生成接口
规范：支持同步与流式输出，集成指数退避重试机制
"""
import aiohttp
import asyncio
from typing import AsyncGenerator, Optional, Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

class LLMEngine:
    """
    AI推理引擎统一接口类
    负责管理与不同模型后端的通信，包括请求封装、流式响应处理和重试逻辑
    """
    def __init__(self, config: Dict[str, Any]):
        """
        初始化引擎
        :param config: 从config.yaml加载的模型配置字典
        """
        self.config = config
        self.model_mode = config.get('model_core', {}).get('run_mode', 'local_api')
        self.session = None  # 延迟初始化aiohttp会话
        self._model_loaded = False

    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建一个异步HTTP会话"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=120)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session

    async def generate_stream(
        self,
        prompt: str,
        context_id: str,
        max_retries: int = 3
    ) -> AsyncGenerator[str, None]:
        """
        流式文本生成接口
        :param prompt: 输入提示词
        :param context_id: 上下文唯一ID，用于跟踪会话
        :param max_retries: 失败重试次数
        :yield: 生成文本片段
        """
        # 1. 校验模型状态（示例）
        if not self._model_loaded:
            # 在实际实现中，这里会检查模型文件或API服务状态
            logger.warning(f"模型未加载，尝试初始化...")
            self._model_loaded = await self._load_model()

        # 2. 根据运行模式选择生成策略
        if self.model_mode == "local_api":
            generator = self._stream_from_local_api(prompt, context_id)
        elif self.model_mode == "cloud_api":
            generator = self._stream_from_cloud_api(prompt, context_id)
        else:  # local_file
            generator = self._stream_from_local_gguf(prompt, context_id)

        # 3. 执行带重试的生成过程
        attempt = 0
        while attempt < max_retries:
            try:
                async for chunk in generator:
                    yield chunk
                break  # 成功完成则退出重试循环
            except Exception as e:
                attempt += 1
                logger.error(f"生成失败 (尝试 {attempt}/{max_retries}): {e}")
                if attempt >= max_retries:
                    raise
                # 指数退避等待
                await asyncio.sleep(1 * (2 ** attempt))

    async def _stream_from_local_api(self, prompt: str, context_id: str) -> AsyncGenerator[str, None]:
        """
        从本地API (如LM Studio) 获取流式响应
        :param prompt: 提示词
        :param context_id: 上下文ID
        :yield: 文本片段
        """
        base_url = self.config['model_core']['local_api']['base_url']
        model_name = self.config['model_core']['local_api']['model_name']
        url = f"{base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "temperature": self.config['model_core']['model_common']['temperature'],
            "max_tokens": self.config['model_core']['model_common']['max_tokens'],
        }

        session = await self._get_session()
        async with session.post(url, json=payload, headers=headers) as response:
            response.raise_for_status()
            # 逐行解析SSE流
            async for line in response.content:
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        data_str = decoded_line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            data_json = json.loads(data_str)
                            if 'choices' in data_json:
                                delta = data_json['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            logger.warning(f"无法解析SSE数据: {data_str}")

    async def _stream_from_cloud_api(self, prompt: str, context_id: str) -> AsyncGenerator[str, None]:
        """从云端API获取流式响应 (实现与本地API类似，但使用不同的配置)"""
        # TODO: 实现云端API调用逻辑
        yield "Cloud API stream placeholder"
        await asyncio.sleep(0)

    async def _stream_from_local_gguf(self, prompt: str, context_id: str) -> AsyncGenerator[str, None]:
        """从本地GGUF模型文件获取流式响应 (使用llama-cpp-python等)"""
        # TODO: 实现本地GGUF模型调用逻辑
        yield "Local GGUF stream placeholder"
        await asyncio.sleep(0)

    async def _load_model(self) -> bool:
        """模拟加载模型的过程，实际实现需检查文件或API连通性"""
        # 实际实现中，这里会验证本地文件存在或API服务可用
        logger.info(f"尝试加载模型，模式: {self.model_mode}")
        return True  # 假设加载成功

    def is_model_loaded(self) -> bool:
        """返回当前模型是否已加载就绪"""
        return self._model_loaded

    def release_context(self, context_id: str) -> None:
        """释放指定上下文占用的资源"""
        logger.info(f"释放上下文: {context_id}")
        # 实际实现中，可能清理缓存或内存中的临时数据
