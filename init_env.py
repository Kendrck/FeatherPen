#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FeatherPen V1.0.0 跨平台环境初始化脚本
功能：Python版本校验、项目必备目录自动创建、批量安装锁定依赖
适配：Windows / Linux / macOS / Android 全平台统一环境初始化
"""

import os
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """
    校验系统Python版本
    强制要求：Python3.14，版本不符直接终止初始化
    """
    version = sys.version_info
    if version.major != 3 or version.minor != 14:
        raise Exception(
            f"环境错误：当前Python版本{version.major}.{version.minor}，项目仅支持Python3.14"
        )


def init_project_dir():
    """
    自动创建项目核心目录
    规避目录缺失导致的日志、数据、配置读写报错
    """
    dir_list = [
        "logs/monitor_log",
        "logs/runtime_log",
        "logs/token_flow_log",
        "Book/User",
        "docs",
    ]
    for dir_path in dir_list:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def install_dependencies():
    """
    批量安装项目锁定依赖
    基于requirements.txt统一安装，保障环境一致性
    """
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )


if __name__ == "__main__":
    check_python_version()
    init_project_dir()
    install_dependencies()
    print("FeatherPen V1.0.0 跨平台环境初始化完成，环境适配正常")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境初始化脚本

一键完成以下操作：
1. 创建 Python 虚拟环境
2. 安装 requirements.txt 依赖
3. 创建必要的运行时目录
4. 生成默认配置文件（如不存在）
"""

import os
import subprocess
import sys
import venv
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 必要目录列表
REQUIRED_DIRS = [
    "data",
    "data/Book",
    "data/database",
    "runtime",
    "runtime/logs",
    "runtime/cache",
    "runtime/temp",
    "assets/lib",
    "assets/fonts",
    "assets/images",
    "docs",
]

# 默认语言包内容
DEFAULT_ZH_CN = {
    "login": {
        "cloud_title": "云端账号登录",
        "uid_input": "8位账号UID",
        "pwd_input": "登录密码",
        "white_btn_tip": "快捷填充测试账号",
    },
    "member": {
        "lv9_switch_title": "Lv9不朽测试账号积分控制开关",
        "switch_on_tip": "当前已开启积分豁免，生成、校正操作不消耗积分",
        "switch_off_tip": "当前已关闭积分豁免，所有操作正常扣除积分",
        "white_label": "白名单测试账号",
        "lv9_label": "不朽特权账号",
    },
}


def create_directories():
    """创建必要的目录结构"""
    print("📁 创建目录结构...")
    for dir_path in REQUIRED_DIRS:
        path = PROJECT_ROOT / dir_path
        path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {dir_path}")


def create_default_locale():
    """创建默认中文语言包"""
    print("🌐 创建默认语言包...")
    locale_path = PROJECT_ROOT / "assets" / "lib" / "zh-CN.json"
    if not locale_path.exists():
        with open(locale_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_ZH_CN, f, ensure_ascii=False, indent=2)
        print("   ✓ zh-CN.json")
    else:
        print("   ✓ zh-CN.json (已存在)")


def create_venv():
    """创建虚拟环境"""
    print("🐍 创建虚拟环境...")
    venv_path = PROJECT_ROOT / "venv"
    if not venv_path.exists():
        venv.EnvBuilder(with_pip=True).create(venv_path)
        print("   ✓ venv/")
    else:
        print("   ✓ venv/ (已存在)")


def install_dependencies():
    """安装依赖包"""
    print("📦 安装依赖...")
    requirements_path = PROJECT_ROOT / "requirements.txt"
    if requirements_path.exists():
        # 确定 pip 路径
        if sys.platform == "win32":
            pip_path = PROJECT_ROOT / "venv" / "Scripts" / "pip.exe"
        else:
            pip_path = PROJECT_ROOT / "venv" / "bin" / "pip"

        subprocess.check_call([str(pip_path), "install", "-r", str(requirements_path)])
        print("   ✓ 依赖安装完成")
    else:
        print("   ⚠ requirements.txt 不存在")


def main():
    """主函数"""
    print("🚀 FeatherPen 环境初始化")
    print("=" * 40)

    try:
        create_directories()
        create_default_locale()
        create_venv()
        install_dependencies()

        print("=" * 40)
        print("✅ 环境初始化完成！")
        print("运行 python main.py 启动应用")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
