# FeatherPen/docs/STRUCTURE.md
# GB/T 8567-2006 FeatherPen V1.0.0 三级架构归档总文档
# 同步基准：世界树.txt、docs/API_MODULE_SPEC.md
# 同步规范文档：docs/dev/Code_And_Doc_Sync_Spec.md
# 强制规范
# 1. 一、二级目录永久锁定，仅允许三级文件/子目录拓展，禁止增删重命名
# 2. 文件/端口/函数/接口变更必须同步更新本文 + API_MODULE_SPEC.md + 世界树.txt
# 3. 仅保留国标业务注释，移除调试/草稿/迭代/临时内容
# 4. 所有路径统一 FeatherPen/ 开头，全程可追溯
# 5. 新增文件同步更新目录树与模块说明
# 6. 交付前校验 Code_And_Doc_Sync_Spec 全部验收条款
## 一、File Path 完整三级文件结构树（与世界树.txt完全一致）
FeatherPen/
├── .gitignore                          # Git忽略：日志、缓存、dist打包产物、runtime临时文件
├── LICENSE                             # MIT开源协议文本
├── pyproject.toml                      # Python构建配置，永久移除Electron/PyQt6依赖
├── requirements.txt                    # 生产运行依赖：uvicorn/fastapi/pywebview/pycryptodome
├── requirements-dev.txt                # 单元测试/打包开发依赖
├── init_env.py                         # 标准化环境初始化，自动创建四级目录、生成标准config.yaml
├── main.py                             # 程序唯一顶层启动入口，顺序初始化库/数据库/后台/前端窗口
├── clean.bat                           # GB/T 8567标准化一键清理脚本，删除缓存/虚拟环境/打包临时文件
├── .github/
│   └── workflows/
│       └── ci_build.yml                # CI跨平台自动打包流水线（Windows/macOS/Linux）
├── docs/
│   ├── README.md                       # 项目快速上手总览文档
│   ├── CHANGELOG.md                    # 全版本迭代变更归档日志
│   ├── STRUCTURE.md                    # 三级架构总归档主文档
│   ├── API_MODULE_SPEC.md              # 端口/函数/接口全局基准规范
│   ├── API.md                          # HTTP离线接口完整手册
│   ├── COMPATIBILITY.md                # Windows/macOS/Linux跨平台国标
│   ├── CONFIG_AND_API_SPEC.md          # 端口加载、通信细则规范
│   ├── DATABASE_SCHEMA.md              # SQLite数据表、索引完整规范
│   ├── DEPLOYMENT_GUIDE.md             # 全平台打包部署操作指南
│   ├── PROJECT_OVERVIEW.md             # 离线隐私、整体项目定位说明
│   ├── ACCOUNT_SPEC.md                 # Lv0~Lv9三层账号校验国标
│   ├── DEVELOP.md                      # 本地开发调试约束规范
│   ├── PRESS_TEST.md                   # 特权UID白名单压测解锁规范
│   ├── local_member_config_v1.0.0.json # 会员等级、权限标准配置模板
│   ├── dev/
│   │   ├── Project_Structure.md        # 开发目录层级解读
│   │   ├── UI_Compatibility_Spec.md    # Web前端跨端兼容规范
│   │   ├── Code_Style.md               # Python/JS编码注释国标
│   │   ├── Test_Guide.md               # 单元编写执行规范
│   │   ├── Build_Guide.md              # Windows打包说明
│   │   └── Code_And_Doc_Spec.md        # 代码与文档同步强制规范
│   ├── user/
│   │   ├── Install_Guide.md            # 用户安装启动教程
│   │   ├── Language_Spec.md            # 多语言配置规范
│   │   ├── Data_Import_Export.md       # 小说工程导入导出规范
│   │   └── FAQ.md                      # 端口/登录/启动报错解决方案
│   └── assets/                         # 文档配图、配置模板资源目录
├── src/
│   ├── __init__.py                     # 后端根包统一导出入口
│   ├── gui/
│   │   ├── __init__.py                 # GUI模块导出标识文件
│   │   └── web_window.py               # PyWebView桌面窗口标准化实现，后端就绪轮询、加载本地web首页
│   ├── server/
│   │   ├── __init__.py                 # Web服务模块导出文件
│   │   └── http_server.py              # FastAPI服务，默认6554端口，基准/api/v1路由
│   ├── account/
│   │   ├── __init__.py                 # 账号模块导出入口
│   │   ├── local_login.py              # 游客/特权UID常量、账号正则三层校验
│   │   ├── member_ctrl.py              # 权限判定（仅白名单拥有积分/压测，Lv9无特权）
│   │   └── point_system.py             # 积分扣减逻辑，白名单自动豁免扣费
│   ├── config/
│   │   ├── __init__.py                 # 配置模块导出入口
│   │   └── config_loader.py            # 读取yaml+环境变量，废弃load_config旧函数
│   ├── core/
│   │   ├── __init__.py                 # AI核心引擎统一导出
│   │   ├── llm_api.py                  # LLM本地推理固定1234端口通信封装
│   │   ├── memory_filter.py            # 历史章节上下文裁剪过滤
│   │   ├── role_extract.py             # 小说人物自动提取、角色卡生成
│   │   ├── novel_auto_gen.py           # 章节批量生成核心，积分权限校验
│   │   ├── world_check.py              # 世界观、剧情一致性校验
│   │   └── progress_monitor.py         # AI生成进度后台监控调度
│   ├── database/
│   │   ├── __init__.py                 # 数据库模块导出入口
│   │   ├── init_db.py                  # SQLite一键初始化执行脚本
│   │   ├── db_sqlite.py                # 账号CRUD，废弃db_get_user_info旧接口
│   │   ├── monitor_db.py               # 硬件/Token监控日志入库
│   │   └── sql_init.sql                # 建表语句+预置10组特权UID账号
│   └── utils/
│       ├── __init__.py                 # 通用工具根包导出
│       ├── monitor/
│       │   ├── monitor_scheduler.py    # AI/硬件监控定时调度器（AI1s/硬件5s）
│       │   └── log_writer.py           # 日志写入、7天自动清理工具
│       ├── process/                    # 跨平台子进程管理工具
│       └── i18n/                       # 全局多语言文本加载工具
├── web/
│   ├── index.html                      # 桌面程序默认登录首页
│   ├── assets/
│   │   ├── css/main.css                # 全局前端统一基础样式
│   │   ├── js/api_client.js            # API请求封装，动态拉取端口、前后端常量对齐
│   │   └── i18n/                       # 多语言JSON文本资源
│   ├── pages/
│   │   ├── login.html                  # 独立登录子页面
│   │   ├── workbench.html              # 6554业务+1234双端口工作台
│   │   ├── member.html                 # 会员等级、压测开关面板
│   │   ├── model_setting.html          # LLM 1234端口可视化配置页
│   │   ├── monitor.html                # AI/硬件实时监控面板
│   │   └── snapshot_export.html        # 快照导出/恢复页面
│   └── public/
│       └── file_handler.js             # 前端本地文件读写工具JS
├── tests/
│   ├── __init__.py                     # 测试根包标识
│   ├── account/                        # 账号、特权权限单元测试脚本
│   └── core/pressure/                  # 压测专项拦截测试用例
├── runtime/
│   ├── logs/
│   │   ├── monitor_log/monitor.log     # 硬件监控持久日志
│   │   ├── runtime_log/runtime.log     # 程序运行日志
│   │   └── token_flow_log/token_flow.log # Token消耗统计日志
│   ├── cache/                          # AI运行临时缓存
│   └── temp/                           # 快照导出临时目录
├── data/
│   ├── Book/
│   │   ├── User/127001/                # Lv0离线游客专属工程目录
│   │   └──【自定义书名】/              # 用户独立小说四级工程
│   │       ├── db/
│   │       ├── chapters/
│   │       ├── vector/
│   │       └── snapshot/
│   └── database/featherpen.db          # 全局SQLite账号数据库
├── assets/
│   ├── lib/                            # 前端第三方JS依赖库
│   ├── fonts/                          # 桌面端专用字体文件
│   └── images/                         # UI图标、插图资源
├── dist/                               # 各平台打包输出产物（exe/dmg/AppImage/deb/rpm）
├── config.yaml                         # 全局端口配置源：Web6554 / LLM1234
├── member_config.json                  # 运行时会员、特权账号配置
├── .env.example                        # 环境变量模板（FP_NETWORK_PREFERRED_PORT）
├── build.bat                           # Windows一键打包脚本
└── setup.bat                           # Windows环境初始化脚本
## 二、全文件标准化注释明细
1. FeatherPen/main.py
注释：程序顶层唯一启动入口，标准化执行链路：环境初始化→数据库初始化→后台API线程→GUI窗口等待服务→加载本地web首页
关联端口：6554、1234
2. FeatherPen/src/gui/__init__.py
注释：GUI模块导出包标识，对外暴露start_gui函数供main调用；基准文档API_MODULE_SPEC.md
3. FeatherPen/src/gui/web_window.py
注释：PyWebView标准化桌面窗口实现；功能：读取配置、轮询/api/v1/ping健康接口、加载本地web/index.html；约束无原生调试控件、无http直连空白页面逻辑
4. FeatherPen/src/server/http_server.py
注释：FastAPI后台服务，监听6554，基准/api/v1，提供/ping健康检测接口
占用端口：6554，监听127.0.0.1
5. FeatherPen/clean.bat
注释：标准化一键清理脚本，清理虚拟环境、打包缓存、py编译缓存、临时草稿日志
6. FeatherPen/config.yaml
注释：全局唯一端口配置中心，禁止硬编码；绑定127.0.0.1，禁用0.0.0.0；仅.env覆盖Web端口
端口参数：network.preferred_port=6554、llm.local_api_port=1234
容错规则：Web端口占用自动分配空闲端口；1234固定无自动分配逻辑
读取依赖：src/config/config_loader.py、src/server/http_server.py、src/core/llm_api.py、web/assets/js/api_client.js、web/pages/model_setting.html
其余原有文件注释保持国标规范，无修改
## 三、GB/T 8567 全局废弃黑名单
### 废弃目录
ui/、electron
### 废弃函数
load_config → load_global_config
db_get_user_info → get_account_info
旧SQLiteDB类
### 废弃业务
8位云端UID、YesApi、cloud_login云端接口
### 废弃UI调试元素（统一文字）
窗口原生【优质打印】调试复选框、后端接口调试JSON返回文本
### 废弃硬编码
直接书写6554/1234数字
### 废弃临时交付文件
*.spec、crash_error.log、all_code.txt、temp_dedup.py、__pycache__、.pyc、.venv/
## 四、V1.0.0 GUI模块+清理脚本 统一变更归档
1. 新增三级目录 src/gui，遵循GB/T 8567一二级锁定、三级拓展规范
2. 新增物理文件：
   FeatherPen/src/gui/__init__.py
   FeatherPen/src/gui/web_window.py
   FeatherPen/clean.bat
3. 配套源码修改：main.py、src/server/http_server.py
4. 模块功能规范：
   仅作为PyWebView桌面窗口承载层，不实现任何业务逻辑；
   内置10秒超时轮询健康接口 /api/v1/ping，规避页面空白问题；
   窗口强制加载本地web/index.html静态资源，禁止直连HTTP地址；
   彻底移除Qt/Electron原生调试控件、调试打印逻辑；
5. 标准化启动链路：
   main.py → init_database() → 后台启动http_server线程 → start_gui轮询ping接口 → 渲染前端首页
6. 后端配套改动：src/server/http新增标准/ping健康接口，日志等级改为error屏蔽冗余输出
7. 文档同步操作：同步更新世界树.txt、API_MODULE_SPEC.md、本文档目录树与变更章节
## 五、分层架构国标说明
1. 后端src：账号/配置/AI/数据库/工具业务层
2. 前端web：纯静态页面，PyWebView容器承载
3. docs：全套国标归档文档，基准为STRUCTURE.md、API_MODULE_SPEC.md
4. tests：单元测试用例
5. runtime：运行缓存、日志
6. data：本地小说、账号持久数据
7. assets：字体、图标静态资源
8. dist：多平台打包产物
## 六、自动初始化国标规范
1. init_env递归创建data/runtime四级目录，缺失自动生成标准config.yaml
2. init_db执行sql_init.sql自动建表、预置10组特权UID
3. 小说工程缺失自动生成db/chapters/vector/snapshot子目录
4. Web端口支持占用自动切换，LLM 1234端口固定不调整
## 七、交付校验引用
所有修改完成后，对照 docs/dev/Code_And_Doc_Sync_Spec.md 交付校验清单逐项验收，全部通过方可打包、合并、交付。