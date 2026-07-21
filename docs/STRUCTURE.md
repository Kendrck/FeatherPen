# FeatherPen/docs/STRUCTURE.md
# FeatherPen V1.0.0 世界树标准仓库完整目录架构文档
# 排序规则：文件夹优先按字母升序，同层级文件按英文字母升序排列
# 注释规范：# 后为文件/文件夹标准化业务说明，强制约束加粗标注
# 文档基准优先级：本目录规范 > 全平台兼容性规范 > 初代开发规范文档

FeatherPen/
├── .github/                      # Github CI/CD自动化流水线目录
│   └── workflows/                # 打包、校验、发布自动化脚本存放目录
│       └── (ci自动脚本yml文件)    # 全平台打包、代码检查、发布流程配置
├── assets/                       # 静态资源根目录，所有前端静态文件统一存放
│   ├── fonts/                    # 程序自定义字体资源
│   ├── images/                   # UI图标、界面图片、封面素材
│   └── lib/                      # 多语言文案包目录【强制】
│       └── zh-CN.json            # 中文简体多语言配置，登录/会员面板文案统一托管，禁止硬编码文字
├── data/                         # 用户持久化业务数据目录
│   ├── Book/                     # 用户创建的小说卷、章、节文本存储目录
│   └── database/                 # SQLite数据库文件存放目录
├── dist/                         # 各平台打包输出产物目录（Windows/macOS/Linux/Android）
├── docs/                         # 项目全套标准化归档文档目录（开发、接口、结构、兼容规范）
│   ├── ACCOUNT_SPEC.md           # 账号体系补充规范文档
│   ├── API.md                    # 后端全接口定义、入参出参、业务逻辑规范
│   ├── CHANGELOG.md              # 版本迭代更新日志
│   ├── COMPATIBILITY.md          # 全平台统一兼容性规范文档
│   ├── CONTRIBUTING.md           # 项目贡献、代码提交规范
│   ├── DEVELOP.md                # 本地开发调试指南、测试账号使用教程
│   ├── README.md                 # 项目快速上手说明文档
│   ├── STRUCTURE.md              # 当前仓库目录标准规范文档（本文件）
│   ├── TEMPLATE.md               # 文档/配置标准化模板文件
│   └── YESAPI_ACCOUNT.md         # YesApi云端10组白名单测试账号对接完整规范
├── runtime/                      # 程序运行时临时生成文件目录
│   ├── cache/                    # AI推理缓存、页面缓存文件
│   ├── logs/                     # 运行日志，系统自动7天清理旧日志
│   └── temp/                     # 临时导出、临时缓存文件
├── sdk/                          # Web/浏览器插件端TS SDK存放目录
│   └── client.ts                 # 前端SDK：测试账号列表、Lv9开关接口封装
├── src/                          # Python后端业务内核源码根目录，UI与业务完全解耦【强制】
│   ├── __init__.py               # Python包初始化标识文件
│   ├── account/                  # 账号、会员、积分扣费核心模块【统一存放，全平台复用】
│   │   ├── __init__.py
│   │   ├── account_login.py      # 云端登录、白名单UID匹配、账号权限下发逻辑
│   │   ├── member_ctrl.py        # 会员等级权限拦截、Lv9特权判定、扣费开关读写
│   │   └── point_system.py       # 积分扣费统一入口、Lv9积分豁免控制逻辑
│   ├── config/                   # 全局配置加载、持久化工具模块
│   │   ├── __init__.py
│   │   └── config_loader.py      # 读取config.yaml、member_config.json，持久化开关配置
│   ├── core/                     # AI长篇小说生成核心引擎（云端API/本地API/GGUF离线三推理模式）
│   │   └── (引擎相关源码文件)
│   ├── database/                 # SQLite持久化数据库初始化、CRUD工具
│   │   └── (数据库操作源码文件)
│   └── utils/                    # 通用工具集：硬件监控、多语言、快照工具
│       └── (工具类源码文件)
├── tests/                        # 单元测试用例目录
│   ├── account/                  # 账号登录、测试账号、Lv9扣费开关专项测试用例
│   └── core/                     # AI生成引擎功能测试用例
├── ui/                           # 客户端图形界面源码目录
│   ├── __init__.py
│   ├── login_ui.py               # 登录窗口页面：内置10个测试账号快捷填充按钮
│   ├── main_window.py            # 程序主窗口入口
│   ├── member_panel.py           # 会员面板：Lv9积分豁免开关+配套多语言提示文字
│   ├── model_setting_ui.py       # AI模型推理模式配置界面
│   └── monitor_dashboard.py      # 硬件+AI进度监控面板（CPU/GPU/内存/Token/进度五维监控）
├── .gitignore                    # Git版本控制忽略文件清单，屏蔽缓存、日志、打包产物、本地配置
├── LICENSE                       # 项目开源许可证文件
├── config.yaml                   # 系统全局运行配置：测试账号总开关、监控参数、签到积分、YesApi密钥
├── init_env.py                   # 跨平台环境一键初始化脚本（依赖、目录、数据库初始化）
├── main.py                       # 项目**唯一全局启动入口**，标准化顺序初始化所有模块
├── member_config.json            # 会员白名单、10组测试账号、Lv9特权配置、各项操作积分消耗定义
├── pyproject.toml                # Python项目标准化构建、打包配置文件
├── requirements-dev.txt          # 开发环境依赖：单元测试、代码格式化、静态检查工具
├── requirements.txt              # 生产环境运行依赖锁定清单


FeatherPen/
├── src/                   # [核心] 业务逻辑层
│   ├── account/           # 账号、权限、积分逻辑
│   ├── config/            # 配置加载器
│   ├── core/              # AI 引擎
│   ├── database/          # 数据持久化
│   └── utils/             # 通用工具
├── ui/                    # [视图] 界面交互层 (PyQt6)
│   ├── login_ui.py        # 登录页 (含测试账号快捷按钮)
│   ├── member_panel.py    # 会员面板 (含 Lv9 开关)
│   └── ...
├── docs/                  # [文档] 标准化说明文档
├── data/                  # [数据] 运行时数据 (数据库、书籍)
├── assets/                # [资源] 图片、多语言包
├── runtime/               # [运行时] 日志、缓存
├── tests/                 # [测试] 单元测试用例
└── main.py                # [入口] 全局唯一启动文件