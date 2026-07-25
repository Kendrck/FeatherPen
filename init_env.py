# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 标准化环境初始化脚本
功能：创建国标三级目录、生成虚拟环境、初始化多语言文件、固定离线游客目录
约束：仅支持Python3.10+，无硬件采集、无系统隐私读取逻辑
"""
import json
import venv
from pathlib import Path

# 项目根路径常量
PROJECT_ROOT = Path(__file__).resolve()

# GB/T 强制运行目录清单（不可删减）
REQUIRED_DIRS = [
    "data/Book/User/127001",
    "data/database",
    "runtime/logs/monitor_log",
    "runtime/logs/runtime_log",
    "runtime/logs/token_flow_log",
    "runtime/cache",
    "runtime/temp",
    "assets/lib",
    "assets/fonts",
    "assets/images",
    "docs",
]

# 默认简体中文语言包内容
DEFAULT_ZH_CN = {
    "login": {
        "uid_input": "6-20位字母数字/_-. 或邮箱，离线游客127001免校验",
        "pwd_input": "密码至少6位，推荐字母数字混合",
        "white_btn_tip": "离线测试账号快捷填充",
    },
    "member": {
        "lv9_switch_title": "Lv9不朽积分豁免开关",
        "switch_on_tip": "开启：生成/校正不扣积分",
        "switch_off_tip": "关闭：正常扣除积分",
        "white_label": "普通离线账号",
        "lv9_label": "Lv9特权账号",
    },
}

def check_python_version():
    """校验Python最低版本3.10，不兼容直接终止初始化"""
    import sys
    ver = sys.version_info
    if ver.major != 3 or ver.minor < 10:
        raise Exception(f"环境不兼容，要求Python3.10及以上，当前版本{ver.major}.{ver.minor}")

def create_standard_dirs():
    """批量创建国标全部运行目录，不存在自动生成"""
    print("【步骤1】创建标准化业务目录")
    for dir_path in REQUIRED_DIRS:
        full_path = PROJECT_ROOT / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"√ {dir_path}")

def init_default_locale():
    """生成默认简体中文语言包assets/lib/zh-CN.json"""
    print("【步骤2】初始化多语言默认配置")
    lang_file = PROJECT_ROOT / "assets/lib/zh-CN.json"
    if not lang_file.exists():
        with open(lang_file, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_ZH_CN, f, ensure_ascii=False, indent=2)
        print("√ assets/lib/zh-CN.json 已新建")
    else:
        print("√ 语言包已存在，跳过创建")

def create_venv_env():
    """创建项目独立虚拟环境venv"""
    print("【步骤3】创建Python虚拟环境")
    venv_path = PROJECT_ROOT / "venv"
    if not venv.exists():
        venv.EnvBuilder(with_pip=True).create(venv_path)
        print("√ 虚拟环境创建完成")
    else:
        print("√ 虚拟环境已存在")

def install_requirements():
    """读取requirements.txt自动安装全部依赖"""
    print("【步骤4】安装项目运行依赖")
    req_file = PROJECT_ROOT / "requirements.txt"
    if not req_file.exists():
        print("× 未找到requirements.txt，跳过依赖安装")
        return
    import subprocess
    import sys
    # 区分系统pip路径
    if sys.platform == "win32":
        pip = venv_path / "Scripts/pip.exe"
    else:
        pip = venv_path / "bin/pip"
    subprocess.check_call([str(pip), "install", "-r", str(req_file)])
    print("√ 全部依赖安装完成")

def init_user_dir():
    """初始化Lv0离线游客user_setting.json默认配置"""
    user_cfg_path = PROJECT_ROOT / "data/Book/User/127001/user_setting.json"
    default_user_cfg = {
        "signin": {"lv9_skip_point_default": False, "lv9_pressure_default": False},
        "database": {"db_path": "featherpen.db"},
        "crypto": {"aes_key": "FeatherPen2026OfflineKey"},
        "model": {"local_api": "http://127.0.0.1:1234/v1", "model_name": "qwen2.5-14b-instruct-1m"}
    }
    if not user_cfg_path.exists():
        with open(user_cfg_path, "w", encoding="utf-8") as f:
            json.dump(default_user_cfg, ensure_ascii=False, indent=2)
        print("√ 离线游客默认配置生成完成")

def main():
    """环境初始化统一入口，无冗余调试输出"""
    try:
        print("==== FeatherPen V1.0.0 标准化离线环境初始化 ====")
        check_python_version()
        create_standard_dirs()
        init_default_locale()
        create_venv_env()
        install_requirements()
        init_user_dir()
        print("\n==== 环境初始化完成，执行 python main.py 启动程序 ====")
    except Exception as err:
        print(f"× 初始化失败：{str(err)}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
