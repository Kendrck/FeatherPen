# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 项目环境标准化初始化脚本
功能：Python版本校验、标准目录创建、虚拟环境生成、依赖批量安装
约束：跨平台兼容 Windows/Linux/macOS，自动生成国标运行目录
"""
import json
import subprocess
import sys
import venv
from pathlib import Path

# 项目根路径全局常量
PROJECT_ROOT = Path(__file__).parent
# 国标强制运行目录清单（三级拓展，一二目录不可修改）
REQUIRED_DIRS = [
    "data",
    "data/Book",
    "data/database",
    "runtime",
    "runtime/cache",
    "runtime/logs",
    "runtime/temp",
    "assets/lib",
    "assets/fonts",
    "assets/images",
    "docs",
]
# 全局默认简体中文语言包
DEFAULT_ZH_CN = {
    "login": {
        "uid_input": "6-20位字母数字/_-. 或邮箱，留空自动主板特权登录",
        "pwd_input": "密码至少6位，推荐字母数字混合",
        "white_btn_tip": "一键填充离线测试账号",
    },
    "member": {
        "lv9_switch_title": "Lv9不朽账号积分豁免开关",
        "switch_on_tip": "已开启豁免，生成/校对不消耗积分",
        "switch_off_tip": "已关闭豁免，所有操作正常扣积分",
        "white_label": "离线测试账号",
        "lv9_label": "Lv9特权账号",
    },
}

def check_python_version():
    """校验运行Python版本，强制3.14，版本不符终止初始化"""
    ver = sys.version_info
    if ver.major != 3 or ver.minor != 14:
        raise Exception(f"环境错误：当前Python{ver.major}.{ver.minor}，项目仅支持Python3.14")

def create_directories():
    """批量创建国标规定全部运行目录，不存在自动生成"""
    print("【步骤1】创建标准项目目录结构")
    for dir_path in REQUIRED_DIRS:
        full_path = PROJECT_ROOT / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"√ {dir_path}")

def create_default_locale():
    """生成默认简体中文国际化配置文件assets/lib/zh-CN.json"""
    print("【步骤2】初始化默认语言包")
    locale_file = PROJECT_ROOT / "assets" / "lib" / "zh-CN.json"
    if not locale_file.exists():
        with open(locale_file, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_ZH_CN, f, ensure_ascii=False, indent=2)
        print("√ assets/lib/zh-CN.json 已新建")
    else:
        print("√ assets/lib/zh-CN.json 已存在，跳过")

def create_venv():
    """生成项目独立虚拟环境venv文件夹"""
    print("【步骤3】创建Python虚拟环境")
    venv_dir = PROJECT_ROOT / "venv"
    if not venv.exists():
        venv.EnvBuilder(with_pip=True).create(venv_dir)
        print("√ venv 虚拟环境创建完成")
    else:
        print("√ venv 已存在，跳过")

def install_dependencies():
    """读取requirements.txt批量安装项目依赖包"""
    print("【步骤4】安装项目全部依赖库")
    req_file = PROJECT_ROOT / "requirements.txt"
    if not req_file.exists():
        print("× requirements.txt 缺失，跳过依赖安装")
        return
    # 区分系统pip路径
    if sys.platform == "win32":
        pip_exe = PROJECT_ROOT / "venv" / "Scripts" / "pip.exe"
    else:
        pip_exe = PROJECT_ROOT / "venv" / "bin" / "pip"
    subprocess.check_call([str(pip_exe), "install", "-r", str(req_file)])
    print("√ 依赖安装完成")

def main():
    """环境初始化统一入口函数"""
    print("==== FeatherPen V1.0.0 标准化环境初始化 ====")
    try:
        check_python_version()
        create_directories()
        create_default_locale()
        create_venv()
        install_dependencies()
        print("==== 全部环境初始化完成，执行 python main.py 启动程序 ====")
    except Exception as e:
        print(f"× 初始化失败：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
