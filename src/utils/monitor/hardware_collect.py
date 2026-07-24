"""
FeatherPen V1.0.0 硬件资源监控采集模块
功能：采集CPU、内存、GPU等硬件指标数据，用于监控仪表盘展示
规范：统一使用psutil和pynvml，无N卡环境自动降级
"""
import logging
from typing import Dict

import psutil
import pynvml

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

"""
GB/T 8567-2006 国标业务注释
文件路径：FeatherPen/src/utils/monitor/hardware_collect.py
功能：读取本地主板硬件序列号，用于本机快速登录
约束：纯本地读取，不上传云端
"""
import sys


def get_mainboard_sn() -> str:
    """
    获取本机主板序列号
    Windows：读取 WMI Win32_BaseBoard
    Linux：读取 /sys/class/dmi/id/board_serial
    macOS：读取 system_profiler SPHardwareSerialNumber
    读取失败兜底返回 "000000"
    """
    try:
        if sys.platform.startswith("win"):
            import wmi
            c = wmi.WMI()
            for board in c.Win32_BaseBoard():
                if board.SerialNumber:
                    return board.SerialNumber.strip().replace("-", "").replace(".", "")
        elif sys.platform.startswith("linux"):
            path = "/sys/class/dmi/id/board_serial"
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip().replace("-", "").replace(".", "")
        elif sys.platform == "darwin":
            import subprocess
            result = subprocess.run(
                ["system_profiler", "SPHardwareDataType"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.splitlines():
                if "Serial Number" in line:
                    return line.split(":")[-1].strip().replace("-", "").replace(".", "")
    except Exception:
        pass

    return "000000"
