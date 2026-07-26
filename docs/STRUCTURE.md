# FeatherPen/docs/STRUCTURE.md
# GB/T 8567-2006 FeatherPen V1.0.0 三级架构归档总文档
# 顶层强制约束
1. 一、二级目录永久锁定，仅允许三级文件/子目录拓展，禁止增删重命名
2. 文件、端口、函数、接口修改必须同步更新本文、API_MODULE_SPEC.md双文档
3. 文档仅保留国标业务注释，删除调试、迭代、草稿、临时冗余内容
4. 全文件路径统一FeatherPen/开头，目录树配套标准化功能注释
5. 新增/删除/重命名三级文件，同步更新File Path树与变更归档清单
## File Path_世界树完整三级文件结构树
FeatherPen/
├── .gitignore                          # Git忽略配置，过滤日志、缓存、打包临时文件
├── LICENSE                             # MIT开源许可文本
├── pyproject.toml                      # Python构建配置，移除Electron/PyQt6依赖
├── requirements.txt                    # 生产依赖：uvicorn/fastapi/pywebview/pycryptodome
├── requirements-dev.txt                # 单元测试开发依赖清单
├── init_env.py                         # 环境初始化，自动创建四级运行目录，写入6554/1234标准端口
├── main.py                             # 程序顶层启动入口，初始化环境、数据库、Web服务、客户端窗口
├── .github/
│   └── workflows/
│       └── ci_build.yml                # CI跨平台自动打包流水线
├── docs/
│   ├── README.md                       # 项目快速上手总览
│   ├── CHANGELOG.md                    # 全版本变更归档日志
│   ├── STRUCTURE.md                    # 三级架构主归档文档
│   ├── API_MODULE_SPEC.md              # 端口/函数/接口全局基准规范
│   ├── API.md                          # HTTP离线接口完整手册
│   ├── COMPATIBILITY.md                # 多系统跨平台兼容国标
│   ├── CONFIG_AND_API_SPEC.md          # 端口通信配置细则
│   ├── DATABASE_SCHEMA.md              # SQLite数据表、索引规范
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
│   │   └── Build_Guide.md              # Windows打包脚本说明
│   ├── user/
│   │   ├── Install_Guide.md            # 用户安装启动教程
│   │   ├── Language_Spec.md            # 前端多语言配置规范
│   │   ├── Data_Import_Export.md       # 小说工程导入导出规范
│   │   └── FAQ.md                      # 端口、登录报错解决方案
│   └── assets/                         # 文档配图、配置模板资源
├── src/
│   ├── __init__.py                     # 后端根包导出入口
│   ├── server/
│   │   └── http_server.py              # FastAPI Web服务，默认6554，基准路由/api/v1
│   ├── account/
│   │   ├── __init__.py
│   │   ├── local_login.py              # 游客、特权UID白名单常量、账号正则校验
│   │   ├── member_ctrl.py              # 会员等级读取、特权UID白名单权限判定（积分/压测唯一依据，Lv9无特权）
│   │   └── point_system.py             # 积分扣减逻辑，白名单UID自动豁免扣费
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_loader.py            # 读取yaml/环境变量加载端口，废弃load_config旧函数
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm_api.py                  # LLM推理通信，固定端口1234
│   │   ├── memory_filter.py            # 对话上下文过滤工具
│   │   ├── role_extract.py             # 小说人物自动提取模块
│   │   ├── novel_auto_gen.py           # AI章节生成核心，依赖1234端口、白名单积分判定
│   │   ├── world_check.py              # 世界观一致性校验
│   │   └── progress_monitor.py         # AI生成进度监控
│   ├── database/
│   │   ├── __init__.py
│   │   ├── init_db.py                  # SQLite一键初始化脚本
│   │   ├── db_sqlite.py                # 账号CRUD封装，废弃db_get_user_info旧方法
│   │   ├── monitor_db.py               # 监控日志持久入库
│   │   └── sql_init.sql                # 建表+预置10组特权UID白名单账号
│   └── utils/
│       ├── __init__.py
│       ├── monitor/
│       │   ├── monitor_scheduler.py    # 硬件监控定时调度
│       │   └── log_writer.py           # 日志脱敏写入工具
│       ├── process/                    # 跨平台子进程管理
│       └── i18n/                       # 全局多语言工具
├── web/
│   ├── index.html                      # 桌面登录首页，依赖6554登录接口
│   ├── assets/
│   │   ├── css/main.css                # 全局前端统一样式
│   │   ├── js/api_client.js            # 前端请求封装，动态拉取端口，常量与后端完全对齐
│   │   └── i18n/                       # 多语言文本资源
│   ├── pages/
│   │   ├── login.html                  # 独立登录页面
│   │   ├── workbench.html              # 双端口6554/1234创作工作台
│   │   ├── member.html                 # 会员、特权开关面板
│   │   ├── model_setting.html          # LLM 1234端口可视化配置
│   │   ├── monitor.html                # AI硬件监控面板
│   │   └── snapshot_export.html        # 快照导出页面
│   └── public/
│       └── file_handler.js             # 前端本地文件读写工具
├── tests/
│   ├── __init__.py
│   ├── account/                        # 账号、特权UID白名单单元测试
│   └── core/pressure/                  # 压测功能专项测试用例
├── runtime/
│   ├── logs/
│   │   ├── monitor_log/monitor.log
│   │   ├── runtime_log/runtime.log
│   │   └── token_flow_log/token_flow.log
│   ├── cache/                          # AI运行临时缓存
│   └── temp/                           # 快照临时导出目录
├── data/
│   ├── Book/
│   │   ├── User/127001/                # Lv0游客专属工程目录
│   │   └──【自定义书名】/              # 用户独立小说四级工程目录
│   │       ├── db/
│   │       ├── chapters/
│   │       ├── vector/
│   │       └── snapshot/
│   └── database/                      # featherpen全局账号库存放目录
├── assets/
│   ├── lib/                            # 前端第三方JS库
│   ├── fonts/                          # 桌面专用字体
│   └── images/                         # UI图标、插图资源
├── dist/
│   ├── FeatherPen_V1.0.0_Windows_Setup.exe
│   ├── FeatherPen_V1.0.0_Windows_Portable.zip
│   ├── FeatherPen_V1.0.0_macOS.dmg
│   ├── FeatherPen_V1.0.0_Linux.AppImage
│   ├── FeatherPen_V1.0.0_amd64.deb
│   ├── FeatherPen_V1.0.0_amd64.rpm
│   ├── FeatherPen_V1.0.0_Web_Docker.zip
│   ├── FeatherPen_V1.0.0_Android.apk
│   └── FeatherPen_V1.0.0_VSCode_Plugin.zip
├── config.yaml                         # 全局端口配置源 Web:6554 LLM:1234
├── member_config.json                  # 特权UID、会员等级配置文件
├── .env.example                        # 环境变量模板 FP_NETWORK_PREFERRED_PORT=6554
├── build.bat                           # Windows一键打包脚本
└── setup.bat                           # Windows环境初始化脚本
## 第二部分 全文件端口归属+标准化注释明细
1. FeatherPen/config.yaml
标准化注释：全局唯一端口配置中心，禁止代码硬编码；绑定127.0.0.1，禁用0.0.0.0；仅.env覆盖Web端口
端口参数：network.preferred_port=6554、llm.local_api_port=1234
容错规则：6554端口占用自动分配空闲端口；1234固定无自动分配逻辑
读取依赖：src/config/config_loader.py、src/server/http_server.py、src/core/llm_api.py、web/assets/js/api_client.js、web/pages/model_setting.html
2. FeatherPen/src/config/config_loader.py
注释：解析yaml+环境变量，非法端口自动回落默认；废弃load_config
关联端口：6554、1234
导出函数：load_global_config()、load_member_config()、save_member_config()
环境变量：FP_NETWORK_PREFERRED_PORT（仅控制Web端口）
3. FeatherPen/src/server/http_server.py
注释：FastAPI后台服务，基准/api/v1，三层账号校验接口
占用端口：6554，监听127.0.0.1
4. FeatherPen/src/core/llm_api.py
注释：LM Studio本地推理HTTP封装，端口永久固定1234
请求模板：http://127.0.0.1:{llm.local_api_port}/v1/chat/completions
5. FeatherPen/src/core/novel_auto_gen.py
注释：AI章节生成业务，依赖1234端口，积分判定仅校验特权UID白名单
6. FeatherPen/web/assets/js/api_client.js
注释：前端请求统一封装，页面初始化动态拉取端口，禁止硬编码；前后端常量完全一致
7. FeatherPen/web/index.html / web/pages/login.html
注释：登录页面，调用6554端口登录接口
8. FeatherPen/web/pages/workbench.html
注释：双端口协同工作台，6554业务接口+1234推理接口
9. FeatherPen/web/pages/model_setting.html
注释：LLM 1234端口可视化配置面板，依赖Web服务接口
10. FeatherPen/main.py
注释：程序顶层启动流程，依次初始化目录、数据库、后台服务
关联端口：6554、1234
11. FeatherPen/init_env.py
注释：缺失config自动写入国标端口，递归创建四级运行目录
默认端口：web=6554 llm=1234
12. FeatherPen/.env.example
注释：Web端口环境变量配置模板
### 无端口依赖文件清单
FeatherPen/src/account/local_login.py
FeatherPen/src/account/member_ctrl.py
FeatherPen/src/account/point_system.py
FeatherPen/src/database/db_sqlite.py
FeatherPen/src/database/sql_init.sql
FeatherPen/src/database/init_db.py
FeatherPen/member_config.json
FeatherPen/web/assets/css/main.css
FeatherPen/web/public/file_handler.js
## 第三部分 GB/T 8567 全局端口强制规范
1. 层级约束：仅三级config.yaml存放端口配置，一二目录禁止新增配置文件
2. 安全约束：所有服务仅本地回环监听，无公网开放逻辑
3. 参数固化：network.preferred_port=6554，llm.local_api_port=1234
4. 容错分层：Web 6554占用自动遍历空闲端口；LLM 1234固定端口不切换
5. 前后统一：前端禁止写死端口数字，全部动态拉取；后端统一调用config_loader
6. 追溯要求：端口/文件变更必须同步STRUCTURE.md、API_MODULE_SPEC.md
## 第四部分 全局废弃黑名单（永久禁用）
### 废弃函数
1. load_config → 替换为load_global_config
2. db_get_user_info → 替换为get_account_info
3. 旧SQLiteDB类
### 废弃业务
8位云端UID、YesApi对接、cloud_login云端登录接口
### 废弃目录
ui/、electron（无代码、无打包分支）
### 废弃硬编码
代码内直接书写6554/1234数字
### 废弃文档
docs/YESAPI_ACCOUNT.md（已物理删除，目录树移除）
## 第五部分 V1.0.0 标准化变更归档清单
1. 移除废弃文档YESAPI_ACCOUNT.md，同步两份架构文档目录树
2. 全局清理8位UID、YesApi、cloud_login、Electron/PyQt6全部冗余描述
3. config_loader废弃load_config，统一标准load_global_config
4. db_sqlite废弃db_get_user_info，统一get_account_info
5. api_client移除端口硬编码，改为/status动态获取
6. init_env新增小说四级目录自动创建逻辑
7. 核心权限重构：取消Lv9自带积分、压测特权；权限唯一依据为PRIVILEGE_UID白名单，Lv9仅扩容章节上限
8. 端口规则分层校准：Web自动分配，LLM端口固定不变
9. 同步更新API_MODULE_SPEC.md目录、函数、接口注释、废弃清单
10. 全docs清理V2草稿、迭代备注，仅保留国标业务注释
## 第六部分 分层架构国标说明
1. 后端业务层 src：账号、数据库、AI生成核心逻辑
2. 前端视图层 web：纯静态HTML/CSS/JS，无后端混写
3. 归档文档层 docs：全套GB/T标准化规范手册
4. 测试质量层 tests：账号、压测专项单元用例
5. 运行支撑层 runtime：日志、缓存、临时文件
6. 持久存储层 data：账号库、小说工程目录
7. 静态资源层 assets：字体、前端第三方资源
8. 产物发布层 dist：全平台安装包、便携压缩包
## 第七部分 自动初始化国标规范
1. init_env递归创建data、runtime四级目录，无config则写入6554/1234标准配置
2. init_db执行sql_init.sql自动建表、预置10组特权UID白名单账号
3. 小说目录缺失自动生成db/chapters/vector/snapshot四级子文件夹
4. Web端口捕获OSError占用异常自动顺延分配；LLM 1234不做抢占处理