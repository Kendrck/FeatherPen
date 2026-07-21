"""
FeatherPen V1.0.0 硬件资源监控采集模块
功能：采集CPU、内存、GPU等硬件指标数据，用于监控仪表盘展示
规范：统一使用psutil和pynvml，无N卡环境自动降级
"""
import psutil
import pynvml
from typing import Dict, Optional
import logging

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 尝试初始化NVML库，用于NVIDIA GPU监控
try:
    pynvml.nvmlInit()
    NVML_AVAILABLE = True
except pynvml.NVMLError:
    NVML_AVAILABLE = False
    logger.warning("NVIDIA NVML库初始化失败，GPU监控功能将不可用")

def get_hardware_metrics() -> Dict[str, float]:
    """
    采集当前硬件资源的核心指标
    :return: 包含cpu_percent, memory_percent, gpu_utilization, vram_percent的字典
    """
    metrics = {
        "cpu_percent": 0.0,
        "memory_percent": 0.0,
        "gpu_utilization": -1.0,  # -1表示不可用
        "vram_percent": -1.0
    }

    # 1. 采集CPU和内存使用率
    try:
        metrics["cpu_percent"] = psutil.cpu_percent(interval=0.5)
        metrics["memory_percent"] = psutil.virtual_memory().percent
    except Exception as e:
        logger.error(f"采集CPU/内存数据失败: {e}")

    # 2. 采集GPU数据（仅在NVML可用时）
    if NVML_AVAILABLE:
        try:
            # 获取第一个NVIDIA GPU的句柄（单卡场景）
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            # 获取GPU利用率
            util_info = pynvml.nvmlDeviceGetUtilizationRates(handle)
            metrics["gpu_utilization"] = util_info.gpu
            # 获取显存使用率
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            metrics["vram_percent"] = (mem_info.used / mem_info.total) * 100
        except pynvml.NVMLError as e:
            logger.error(f"采集GPU数据失败: {e}")
            # 发生错误时重置GPU状态为不可用
            metrics["gpu_utilization"] = -1.0
            metrics["vram_percent"] = -1.0

    return metrics

def get_gpu_availability() -> bool:
    """
    检查系统是否有可用的NVIDIA GPU
    :return: 有可用NVIDIA GPU返回True，否则返回False
    """
    return NVML_AVAILABLE and pynvml.nvmlDeviceGetCount() > 0
