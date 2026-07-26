# FeatherPen/docs/API_MODULE_SPEC.md
# GB/T 8567-2006 V1.0.0 软件模块、端口、接口统一基准文档
# 同步基准：世界树.txt、docs/STRUCTURE.md
# 同步规范文档：docs/dev/Code_And_Doc_Sync_Spec.md
# 同步强制规则：修改端口/函数/接口/文件，同步更新本文 + STRUCTURE.md + 世界树.txt
# 约束：仅国标业务注释，删除调试、草稿、临时冗余内容
# 第一部分 File Path_完整三级文件结构树（与世界树、STRUCTURE完全一致）
FeatherPen/
├── .gitignore                          # Git忽略日志、缓存、dist打包产物、runtime临时文件
├── LICENSE                             # MIT开源协议文本
├── pyproject.toml                      # Python构建配置，移除Electron/PyQt6依赖
├── requirements.txt                    # 生产依赖：uvicorn/fastapi/pywebview/pycryptodome
├── requirements-dev.txt                # 单元测试开发依赖
├── init_env.py                         # 环境初始化，自动创建四级目录、写入6554/1234端口
├── main.py                             # 程序顶层启动入口
├── clean.bat                           # GB/T 8567标准化一键清理脚本，删除缓存/虚拟环境/打包临时文件
├── .github/
│   └── workflows/
│       └── ci_build.yml                # CI跨平台自动打包流水线
├── docs/
│   ├── README.md                       # 项目快速上手总览
│   ├── CHANGELOG.md                    # 版本变更归档日志
│   ├── STRUCTURE.md                    # 三级架构主归档文档
│   ├── API_MODULE_SPEC.md              # 端口/函数/接口全局基准文档
│   ├── API.md                          # HTTP离线接口完整手册
│   ├── COMPATIBILITY.md                # 多系统跨平台兼容国标
│   ├── CONFIG_AND_API_SPEC.md          # 端口通信配置细则
│   ├── DATABASE_SCHEMA.md              # SQLite数据表规范
│   ├── DEPLOYMENT_GUIDE.md             # 多平台打包部署指南
│   ├── PROJECT_OVERVIEW.md             # 项目离线隐私整体规范
│   ├── ACCOUNT_SPEC.md                 # Lv0~Lv9账号三层校验国标
│   ├── DEVELOP.md                      # 本地开发调试规范
│   ├── PRESS_TEST.md                   # 特权UID白名单压测规范
│   ├── local_member_config_v1.0.0.json # 会员权限标准配置模板
│   ├── dev/
│   │   ├── Project_Structure.md        # 开发目录层级解读
│   │   ├── UI_Compatibility_Spec.md    # Web前端跨端兼容规范
│   │   ├── Code_Style.md               # Python/JS编码注释国标
│   │   ├── Test_Guide.md               # 单元测试执行规范
│   │   ├── Build_Guide.md              # Windows打包说明
│   │   └── Code_And_Doc_Spec.md        # 代码文档同步强制规范
│   ├── user/
│   │   ├── Install_Guide.md            # 用户安装教程
│   │   ├── Language_Spec.md            # 多语言配置规范
│   │   ├── Data_Import_Export.md       # 工程导入导出规范
│   │   └── FAQ.md                      # 端口、登录报错解决方案
│   └── assets/                         # 文档配图、配置资源
├── src/
│   ├── __init__.py                     # 后端根包导出入口
│   ├── gui/
│   │   ├── __init__.py                 # GUI模块导出标识
│   │   └── web_window.py               # PyWebView窗口、服务就绪轮询实现
│   ├── server/
│   │   ├── __init__.py                 # Web服务模块导出文件
│   │   └── http_server.py              # FastAPI Web服务，默认6554，基准/api/v1
│   ├── account/
│   │   ├── __init__.py                 # 账号模块导出入口
│   │   ├── local_login.py              # 游客、特权UID白名单常量、账号正则
│   │   ├── member_ctrl.py              # 权限判定，Lv9无积分/压测特权
│   │   └── point_system.py             # 积分扣减，白名单自动豁免
│   ├── config/
│   │   ├── __init__.py                 # 配置模块导出入口
│   │   └── config_loader.py            # 读取yaml/env，废弃load_config
│   ├── core/
│   │   ├── __init__.py                 # AI核心模块导出
│   │   ├── llm_api.py                  # LLM推理固定1234端口
│   │   ├── memory_filter.py            # 上下文过滤工具
│   │   ├── role_extract.py             # 角色提取模块
│   │   ├── novel_auto_gen.py           # AI章节生成，积分权限校验
│   │   ├── world_check.py              # 世界观一致性校验
│   │   └── progress_monitor.py         # AI生成进度监控
│   ├── database/
│   │   ├── __init__.py                 # 数据库模块导出
│   │   ├── init_db.py                  # SQLite初始化脚本
│   │   ├── db_sqlite.py                # 账号CRUD，废弃db_get_user_info
│   │   ├── monitor_db.py               # 监控日志入库
│   │   └── sql_init.sql                # 建表+预置10组特权账号
│   └── utils/
│       ├── __init__.py                 # 工具根包导出
│       ├── monitor/
│       │   ├── monitor_scheduler.py    # 硬件/AI监控定时调度器
│       │   └── log_writer.py           # 日志写入、7天清理
│       ├── process/                    # 跨平台子进程工具
│       └── i18n/                       # 全局多语言工具
├── web/
│   ├── index.html                      # 桌面登录首页
│   ├── assets/
│   │   ├── css/main.css                # 前端全局统一样式
│   │   ├── js/api_client.js            # API请求封装，动态拉取端口
│   │   └── i18n/                       # 多语言JSON文本资源
│   ├── pages/
│   │   ├── login.html                  # 独立登录子页面
│   │   ├── workbench.html              # 6554/1234双端口工作台
│   │   ├── member.html                 # 会员特权面板
│   │   ├── model_setting.html          # LLM端口配置页
│   │   ├── monitor.html                # AI/硬件监控面板
│   │   └── snapshot_export.html        # 快照导出页面
│   └── public/
│       └── file_handler.js             # 前端本地文件读写JS
├── tests/
│   ├── __init__.py                     # 测试根包
│   ├── account/                        # 账号单元测试
│   └── core/pressure/                  # 压测专项测试用例
├── runtime/
│   ├── logs/
│   │   ├── monitor_log/monitor.log
│   │   ├── runtime_log/runtime.log
│   │   └── token_flow_log/token_flow.log
│   ├── cache/                          # AI运行临时缓存
│   └── temp/                           # 快照临时目录
├── data/
│   ├── Book/
│   │   ├── User/127001/                # Lv0游客工程
│   │   └──【自定义书名】/db/chapters/vector/snapshot
│   └── database/featherpen.db          # 全局SQLite账号数据库
├── assets/
│   ├── lib/                            # 前端第三方JS库
│   ├── fonts/                          # 桌面字体
│   └── images/                         # UI图标
├── dist/                               # 打包产物
├── config.yaml                         # Web6554 / LLM1234端口配置源
├── member_config.json                  # 会员、特权账号配置
├── .env.example                        # 环境变量模板
├── build.bat                           # Windows打包脚本
└── setup.bat                           # Windows环境初始化脚本
## 第二部分 全文件标准化明细（端口/文件/导出函数/HTTP接口）
### 1 FeatherPen/config.yaml
文件路径：FeatherPen/config.yaml
占用端口：network.preferred_port=6554、llm.local_api_port=1234
绑定地址：127.0.0.1
环境变量：FP_NETWORK_PREFERRED_PORT
读取依赖文件：main.py、src/gui/web_window.py、src/server/http_server.py、src/config/config_loader.py、src/core/llm_api.py、web/assets/js/api_client.js
### 2 FeatherPen/src/config/config_loader.py
文件路径：FeatherPen/src/config/config_loader.py
关联端口：6554、1234
导出函数：load_global_config()、load_member_config()、save_member_config()
废弃函数：load_config
### 3 FeatherPen/src/server/http_server.py
文件路径：FeatherPen/src/server/http_server.py
占用端口：6554
监听地址：127.0.0.1
导出函数：run_server()
标准接口：GET /api/v1/ping
业务接口：GET /api/v1/status、POST /api/v1/user/login
### 4 FeatherPen/src/gui/__init__.py
文件路径：FeatherPen/src/gui/__init__.py
端口：无
导出函数：start_gui
### 5 FeatherPen/src/gui/web_window.py
文件路径：FeatherPen/src/gui/web_window.py
关联端口：6554
依赖接口：GET /api/v1/ping
核心导出函数：wait_backend_service()、create_standard_window()、start_gui()
### 6 FeatherPen/main.py
文件路径：FeatherPen/main.py
关联端口：6554、1234
标准执行流程：init_database → 后台启动http_server → start_gui等待服务 → 加载本地首页
### 7 FeatherPen/clean.bat
文件路径：FeatherPen/clean.bat
端口：无
功能：一键清理虚拟环境、打包缓存、py编译缓存、临时日志草稿
### 8 FeatherPen/src/account/local_login.py
文件路径：FeatherPen/src/account/local_login.py
端口：无
全局常量：OFFLINE_GUEST_UID="127001"、PRIVILEGE_UID数组
### 9 FeatherPen/src/account/member_ctrl.py
文件路径：FeatherPen/src/account/member_ctrl.py
端口：无
导出函数：get_user_level()、is_privilege_uid()、toggle_point_deduct_switch()、unlock_pressure_mode()
### 10 FeatherPen/src/account/point_system.py
文件路径：FeatherPen/src/account/point_system.py
端口：无
导出函数：consume_point()
### 11 FeatherPen/src/core/llm_api.py
文件路径：FeatherPen/src/core/llm_api.py
通信端口：1234
导出函数：llm_client.generate_text()
### 12 FeatherPen/src/core/novel_auto_gen.py
文件路径：FeatherPen/src/core/novel_auto_gen.py
依赖端口：1234
关联接口：POST /api/v1/novel/gen_chapter
### 13 FeatherPen/web/assets/js/api_client.js
文件路径：FeatherPen/web/assets/js/api_client.js
基准地址：http://127.0.0.1:{web_port}/api/v1
规范：禁止硬编码端口，动态拉取
## 第三部分 全局HTTP接口基准 /api/v1
### 系统基础接口
GET /api/v1/ping 窗口服务检测
GET /api/v1/status 运行信息获取
### 用户账号模块
POST /api/v1/user/login
GET /api/v1/user/check_name
GET /api/v1/user/info
POST /api/v1/user/register
### 会员积分模块
GET /api/v1/member/level_config
POST /api/v1/toggle_lv9_deduct
### AI生成模块
POST /api/v1/novel/gen_chapter
POST /api/v1/novel/gen_role
POST /api/v1/novel/gen_timeline
POST /api/v1/novel/world_check
### 快照/监控配置
GET /api/v1/snapshot/list
POST /api/v1/snapshot/export
POST /api/v1/snapshot/import
GET /api/monitor/hardware
GET /api/monitor/token_stat
GET /api/monitor/progress
GET /api/config/network_info
## 第四部分 统一错误码
200 正常
400 参数非法
401 账号校验失败
403 权限不足
500 服务异常
## 第五部分 编码命名国标
Python：函数snake_case，类PascalCase，常量全大写
JS：函数camelCase，常量全大写
HTTP：GET查询，POST提交，PUT更新，DELETE删除
## 第六部分 GB/T 8567 全局端口强制规范
1. 一二级目录锁定，端口仅在config.yaml统一配置
2. 所有服务仅监听127.0.0.1本地回环
3. Web默认6554，冲突自动换端口；LLM永久固定1234
4. 前端禁止硬编码端口，通过/status动态获取
5. 文件/函数/端口修改必须同步三份架构文档
## 第七部分 GUI模块通信规范
1. 模块路径：FeatherPen/src/gui
2. 依赖库：pywebview>=4.0
3. 仅页面容器，无业务逻辑，依靠/ping检测后端
4. 10秒连接超时，写入crash_error.log
5. 强制读取本地web/index.html，禁止HTTP直连页面
6. 移除Qt/Electron全部调试控件、调试输出
7. 永久禁止ui/、electron目录
## 第八部分 全局废弃黑名单
### 废弃目录
ui/、electron
### 废弃函数
load_config、db_get_user_info
### 废弃业务
云端账号、YesApi、cloud_login
### 废弃调试内容
窗口【优质打印】复选框、后端调试JSON返回文本
### 废弃硬编码
直接写6554、1234数字
### 废弃临时文件
*.spec、crash_error.log、all_code.txt、temp_dedup.py、.venv、__pycache__、.pyc
## 第九部分 V1.0.0变更归档
1. 新增三级目录 src/gui
2. 新增文件：src/gui/__init__.py、src/gui/web_window.py、clean.bat
3. 修改源码：main.py、src/server/http_server.py
4. 同步更新：世界树.txt、STRUCTURE.md、本文档目录树与明细
5. 校验依据：docs/dev/Code_And_Doc_Sync_Spec.md