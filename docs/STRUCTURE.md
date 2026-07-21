# STRUCTURE.md FeatherPen世界树仓库目录标准 V1.0.0
优先级：本文档 > 迭代临时文档，所有代码目录必须严格遵循
```text
FeatherPen/
├── .gitignore               # Git版本控制忽略规则
├── .gitattributes           # Git LFS大文件追踪配置
├── LICENSE                  # 开源许可证文件
├── pyproject.toml           # Python项目标准化构建配置
├── requirements.txt         # 生产环境依赖锁定清单
├── requirements-dev.txt     # 开发环境依赖：单元测试、格式化、静态检查
├── init_env.py              # 跨平台环境一键初始化脚本
├── main.py                  # 项目唯一全局启动入口
├── .github/
│   └── workflows/           # CI/CD打包发布自动化脚本
├── docs/                    # 全套项目标准化文档
│   ├── YESAPI_ACCOUNT.md    # YesApi云端白名单测试账号对接文档
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── STRUCTURE.md
│   ├── DEVELOP.md
│   ├── API.md
│   ├── COMPATIBILITY.md
│   ├── CONTRIBUTING.md
│   └── TEMPLATE.md
├── src/                     # 业务逻辑内核（与UI完全解耦）
│   ├── __init__.py
│   ├── account/             # 账号、会员、积分扣费模块
│   │   ├── __init__.py
│   │   ├── account_login.py # 云端账号校验、登录逻辑
│   │   ├── member_ctrl.py   # 会员等级、Lv9特权判定
│   │   └── point_system.py  # 积分扣费计算逻辑
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_loader.py # 全局配置yaml/json加载器
│   ├── core/                # AI小说生成核心引擎
│   ├── database/            # SQLite本地持久化层
│   └── utils/               # 通用工具、日志、多语言
├── ui/                      # 客户端界面层，纯视图逻辑
│   ├── __init__.py
│   ├── main_window.py       # 主窗口容器
│   ├── login_ui.py          # 登录弹窗（10个测试账号快捷按钮）
│   ├── novel_workbench.py   # 小说创作工作台
│   ├── member_panel.py      # Lv9积分开关会员面板
│   ├── model_setting_ui.py  # AI模型参数配置界面
│   └── monitor_dashboard.py # 硬件&AI运行监控面板
├── tests/                   # 单元测试目录，镜像src分层
│   ├── account/
│   └── core/
├── runtime/                 # 运行自动生成，.gitignore屏蔽
│   ├── logs/
│   ├── cache/
│   └── temp/
├── data/                    # 用户私有小说数据，不上传仓库
│   ├── Book/
│   └── database/
├── assets/                  # 程序静态资源，必须入库
│   ├── lib/                 # 多语言翻译文案包
│   ├── fonts/
│   └── images/
└── dist/                    # 打包产物，推荐使用GitHub Releases分发