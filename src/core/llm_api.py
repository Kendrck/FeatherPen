# -*- coding: utf-8 -*-
"""
FeatherPen 终极多模型统一调用核心
功能说明：
1. 支持三模型自由切换：local_api / cloud_api / local_file
2. 完全兼容 LM Studio 1234 /v1 标准接口
3. 适配云端OpenAI兼容接口、本地GGUF裸模型离线推理
4. 静默运行，无端口、URL强制校验拦截
5. 修复全版本已知BUG，全模型可正常使用
"""
import requests
import time
import llama_cpp
from config.config_loader import global_cfg

class LLMUniversalClient:
    def __init__(self):
        # 读取全局模型运行模式
        self.run_mode = global_cfg.get_ini("model_core", "run_mode")

        # 本地API模型配置（LM Studio/OpenAI兼容接口）
        self.local_base = global_cfg.get_ini("local_api", "base_url").strip()
        self.local_model = global_cfg.get_ini("local_api", "model_name")
        self.local_key = global_cfg.get_ini("local_api", "api_key")

        # 云端API模型配置
        self.cloud_base = global_cfg.get_ini("cloud_api", "base_url").strip()
        self.cloud_model = global_cfg.get_ini("cloud_api", "model_name")
        self.cloud_key = global_cfg.get_ini("cloud_api", "api_key")
        self.cloud_timeout = int(global_cfg.get_ini("cloud_api", "timeout"))

        # 本地GGUF裸模型文件配置
        self.gguf_path = global_cfg.get_ini("local_file", "gguf_path").strip()
        self.ctx_len = int(global_cfg.get_ini("local_file", "ctx_len"))
        self.threads = int(global_cfg.get_ini("local_file", "threads"))
        self.gpu_layers = int(global_cfg.get_ini("local_file", "n_gpu_layers"))
        self.local_gguf_model = None

        # 全局通用生成参数
        self.temp = float(global_cfg.get_ini("model_common", "temperature"))
        self.max_tokens = int(global_cfg.get_ini("model_common", "max_tokens"))
        self.top_p = float(global_cfg.get_ini("model_common", "top_p"))

    def check_service(self):
        """静默服务状态检测
