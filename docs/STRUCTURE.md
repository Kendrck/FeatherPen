# FeatherPen/docs/STRUCTURE.md
# FeatherPen V1.0.0 三级架构归档总文档
# 执行标准：GB/T 8567-2006《计算机软件文档编制规范》
# 顶层硬性约束
# 1. 一、二级目录永久锁定，仅允许三级文件/子目录拓展，禁止增删改名
# 2. 所有文件、端口、函数、接口改动必须同步更新本文 + docs/API_MODULE_SPEC.md 双文档
# 3. 代码仅保留国标业务注释，删除调试、迭代、临时、废弃冗余内容
# 4. 文件完整路径统一 FeatherPen/ 开头，目录树配套标准化功能注释、端口标识
# 5. 新增/删除/重命名三级文件必须同步更新File Path树与变更归档清单

## File Path_世界树完整三级文件结构树（补全四级小说工程子目录、dist打包产物、init_db.py）
FeatherPen/
├── .gitignore                          # Git忽略配置，屏蔽日志、缓存、打包、临时文件
├── LICENSE                             # MIT开源协议文本
├── pyproject.toml                      # Python构建配置，彻底移除Electron/PyQt6依赖
├── requirements.txt                    # 生产依赖：uvicorn/fastapi/pywebview/pycryptodome
├── requirements-dev.txt                # 单元测试、开发调试依赖清单
├── init_env.py                         # 环境初始化：自动创建全套运行目录，缺失config写入默认端口6554/1234
├── main.py                             # 程序唯一启动入口，加载配置、初始化库、后台启动FastAPI、唤起PyWebView
├── .github/
│   └── workflows/
│       └── ci_build.yml                # 跨平台CI自动打包流水线脚本
├── docs/
│   ├── README.md                       # 项目快速上手总览文档
│   ├── CHANGELOG.md                    # 全版本迭代变更日志
│   ├── STRUCTURE.md                    # 【主架构归档文件】本文件，存储完整世界树、端口、变更记录
│   ├── API.md                          # HTTP接口完整请求/响应手册
│   ├── API_MODULE_SPEC.md              # 端口/函数/接口全局唯一基准文档
│   ├── COMPATIBILITY.md                # Windows/macOS/Linux跨平台兼容规范
│   ├── CONFIG_AND_API_SPEC.md          # 网络端口、通信参数国标细则
│   ├── DATABASE_SCHEMA.md              # SQLite数据表、索引、约束完整规范
│   ├── DEPLOYMENT_GUIDE.md             # 多平台打包部署操作指南
│   ├── PROJECT_OVERVIEW.md             # 项目定位、离线隐私说明
│   ├── ACCOUNT_SPEC.md                 # Lv0~Lv9三层账号校验规范
│   ├── YESAPI_ACCOUNT.md               # 云端账号预留文档(V1.0暂不实现)
│   ├── PRESS_TEST.md                   # Lv9特权压测解锁规则
│   ├── local_member_config_v1.0.0.json # 会员权限标准模板配置
│   ├── dev/
│   │   ├── Project_Structure.md        # 开发目录层级解读文档
│   │   ├── UI_Compatibility_Spec.md    # Web前端跨端兼容规范
│   │   ├── Code_Style.md               # Python/JS国标注释编码规范
│   │   ├── Test_Guide.md               # 单元测试编写执行规范
│   │   └── Build_Guide.md              # Windows打包脚本使用说明
│   ├── user/
│   │   ├── Install_Guide.md            # 普通用户安装启动教程
│   │   ├── Language_Spec.md            # 前端i18n多语言配置规范
│   │   ├── Data_Import_Export.md       # 小说工程导入导出规范
│   │   └── FAQ.md                      # 端口冲突、登录报错解决方案
│   └── assets/                         # 文档配图、配置模板存放目录
├── src/
│   ├── __init__.py                     # 后端根包导出入口
│   ├── server/
│   │   └── http_server.py              # FastAPI主服务，占用默认端口6554，承载/api/v1全接口
│   ├── account/
│   │   ├── __init__.py                 # 账号模块导出入口
│   │   ├── local_login.py              # 游客127001/6位特权账号校验，无网络端口依赖
│   │   ├── member_ctrl.py              # 会员等级、Lv9积分开关控制，无端口依赖
│   │   └── point_system.py             # AI生成积分扣减逻辑，无端口依赖
│   ├── config/
│   │   ├── __init__.py                 # 配置模块导出入口
│   │   └── config_loader.py            # 读取config.yaml，获取6554/1234端口，废弃load_config
│   ├── core/
│   │   ├── __init__.py                 # AI核心模块导出入口
│   │   ├── llm_api.py                  # LM Studio通信，默认推理端口1234
│   │   ├── memory_filter.py            # 对话上下文过滤，无端口依赖
│   │   ├── role_extract.py             # 小说角色自动提取，无端口依赖
│   │   ├── novel_auto_gen.py           # 小说生成业务，依赖1234 LLM端口
│   │   ├── world_check.py              # 世界观一致性校验，无端口依赖
│   │   └── progress_monitor.py         # AI生成进度后台监控，无端口依赖
│   ├── database/
│   │   ├── __init__.py                 # 数据库模块导出入口
│   │   ├── init_db.py                  # 数据库一键初始化，自动执行sql_init.sql（新增补全）
│   │   ├── db_sqlite.py                # SQLite账号CRUD，废弃db_get_user_info，无网络端口
│   │   ├── monitor_db.py               # 硬件监控日志入库，无网络端口
│   │   └── sql_init.sql                # 建表+Lv0-Lv9十级账号初始化脚本
│   └── utils/
│       ├── __init__.py
│       ├── monitor/
│       │   ├── monitor_scheduler.py    # 硬件监控定时调度任务，无端口
│       │   └── log_writer.py           # 日志脱敏输出，屏蔽密钥账号明文
│       ├── process/                    # 跨平台子进程管理工具
│       └── i18n/                       # 全局多语言翻译工具
├── web/
│   ├── index.html                      # 桌面登录首页，依赖6554 Web端口
│   ├── assets/
│   │   ├── css/main.css                # 全局统一前端样式
│   │   ├── js/api_client.js            # 前端请求封装，动态读取端口，禁止硬编码数字（修正描述）
│   │   └── i18n/                       # 多语言文本资源目录
│   ├── pages/
│   │   ├── login.html                  # 独立登录页面，调用6554登录接口
│   │   ├── workbench.html              # 创作工作台，同时使用6554、1234双端口
│   │   ├── member.html                 # 会员积分、特权面板
│   │   ├── model_setting.html          # LLM 1234端口可视化配置页面
│   │   ├── monitor.html                # AI/硬件实时监控面板
│   │   └── snapshot_export.html        # 小说工程快照导出页面
│   └── public/
│       └── file_handler.js             # 前端本地文件读写工具JS
├── tests/
│   ├── __init__.py
│   ├── account/                        # 账号校验单元测试用例
│   └── core/pressure/                  # Lv9压测专项单元测试
├── runtime/
│   ├── logs/
│   │   ├── monitor_log/monitor.log    # 硬件监控持久日志
│   │   ├── runtime_log/runtime.log    # 程序运行主日志
│   │   └── token_flow_log/token_flow.log # Token消耗统计日志
│   ├── cache/                          # AI运行临时缓存目录
│   └── temp/                           # 快照临时导出目录
├── data/
│   ├── Book/
│   │   ├── User/127001/                # Lv0离线游客专属自动生成目录
│   │   └──【自定义书名】/              # 用户独立小说工程（四级子目录补全）
│   │       ├── db/                     # 单本小说本地小型数据库
│   │       ├── chapters/               # 章节正文文本存储
│   │       ├── vector/                 # 文本向量缓存目录
│   │       └── snapshot/               # 工程备份快照目录
│   └── database/                      # 全局账号数据库featherpen.db存放目录
├── assets/
│   ├── lib/                            # 前端第三方静态JS库
│   ├── fonts/                          # 桌面端专用字体资源
│   └── images/                         # UI图标、插图资源
├── dist/                               # 全平台打包产物目录（补全细分打包文件）
│   ├── FeatherPen_V1.0.0_Windows_Setup.exe
│   ├── FeatherPen_V1.0.0_Windows_Portable.zip
│   ├── FeatherPen_V1.0.0_macOS.dmg
│   ├── FeatherPen_V1.0.0_Linux.AppImage
│   ├── FeatherPen_V1.0.0_amd64.deb
│   ├── FeatherPen_V1.0.0_amd64.rpm
│   ├── FeatherPen_V1.0.0_Web_Docker.zip
│   ├── FeatherPen_V1.0.0_Android.apk
│   ├── FeatherPen_V1.0.0_Chrome_Plugin.zip
│   └── FeatherPen_V1.0.0_VSCode_Plugin.zip
├── config.yaml                         # 全局唯一端口配置源：6554/1234，绑定127.0.0.1
├── member_config.json                  # 6位特权账号配置，无端口相关字段
├── .env.example                        # 环境变量模板：FP_NETWORK_PREFERRED_PORT=6554
├── build.bat                           # Windows一键打包脚本
└── setup.bat                           # Windows本地环境初始化脚本

## 第二部分 全文件端口归属+标准化注释明细（补全环境变量、容错规则）
1. FeatherPen/config.yaml
标准化功能注释：全局中心化端口唯一配置文件，禁止任何代码硬编码端口；绑定IP固定127.0.0.1，禁用0.0.0.0公网监听；支持.env环境变量覆盖Web端口。
内置端口配置：network.preferred_port=6554（Web主端口），llm.local_api_port=1234（AI推理端口）
冲突容错：启动捕获端口占用OSError，自动分配空闲端口并打印控制台日志
读取依赖文件：src/config/config_loader.py、src/server/http_server.py、src/core/llm_api.py、web/assets/js/api_client.js、web/pages/model_setting.html

2. FeatherPen/src/config/config_loader.py
标准化功能注释：统一解析yaml与.env变量，内置端口数值合法性校验，非法值自动回落6554/1234；废弃旧函数load_config，标准导出load_global_config/load_member_config/save_member_config
关联端口：6554、1234
环境变量标识：FP_NETWORK_PREFERRED_PORT

3. FeatherPen/src/server/http_server.py
标准化功能注释：FastAPI后台服务，监听6554端口，基准路由/api/v1，实现三层账号登录接口；端口占用自动顺延分配
占用端口：6554
监听地址：127.0.0.1

4. FeatherPen/src/core/llm_api.py
标准化功能注释：对接本地LM Studio服务，动态读取1234推理端口，标准OpenAI兼容请求地址
通信端口：1234
请求地址模板：http://127.0.0.1:{llm.local_api_port}/v1/chat/completions

5. FeatherPen/src/core/novel_auto_gen.py
标准化功能注释：小说生成业务层，内部调用llm_api，依赖1234推理端口
关联端口：1234

6. FeatherPen/web/assets/js/api_client.js
标准化功能注释：前端全局请求封装，动态从/api/status获取当前Web端口，彻底删除硬编码数字
请求前缀模板：http://127.0.0.1:{web_port}/api/v1
关联端口：6554

7. FeatherPen/web/index.html / web/pages/login.html
标准化功能注释：登录页面，调用POST /api/v1/user/login接口，依赖6554端口
关联端口：6554

8. FeatherPen/web/pages/workbench.html
标准化功能注释：创作主界面，同时向后端6554、本地AI 1234发起请求
关联端口：6554、1234

9. FeatherPen/web/pages/model_setting.html
标准化功能注释：可视化修改llm.local_api_port并持久写入config.yaml，页面接口依赖6554
关联端口：6554、1234

10. FeatherPen/main.py
标准化功能注释：顶层启动入口，顺序初始化目录、数据库、Web服务；拉起桌面窗口访问本地服务
关联端口：6554、1234

11. FeatherPen/init_env.py
标准化功能注释：缺失config.yaml自动填充6554/1234默认端口；递归创建全套运行四级目录
默认写入端口：web=6554、llm=1234

12. FeatherPen/.env.example
标准化功能注释：环境变量覆盖模板，可外部覆盖Web服务端口
变量：FP_NETWORK_PREFERRED_PORT=6554

## 无网络端口依赖完整文件清单
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
1. 层级约束：端口配置仅存放三级文件config.yaml，一二目录禁止新增配置文件
2. 安全约束：所有服务仅监听127.0.0.1，无外网开放逻辑
3. 固化端口命名：network.preferred_port=6554，llm.local_api_port=1234
4. 容错机制：端口占用自动分配空闲端口并输出日志；配置缺失自动填充国标默认值
5. 前后端统一：前端禁止手写端口数字，运行时动态获取；后端统一通过config_loader读取
6. 追溯规则：端口/文件改动必须同步更新本文+API_MODULE_SPEC.md

## 第四部分 全局废弃黑名单（完整补全，同步两份文档）
### 废弃函数（全项目删除调用）
1. load_config → 标准名称 load_global_config
2. db_get_user_info → 标准名称 get_account_info
3. SQLiteDB 数据库封装类（永久移除）
### 废弃账号规则
8位数字UID全套校验逻辑，仅保留127001游客 + 000000~999999六位特权账号
### 废弃目录
ui/、electron/（项目全程不创建，代码无相关导入）
### 废弃硬编码规范
代码中禁止直接书写6554、1234数字常量

## 第五部分 V1.0.0 标准化变更归档清单（补全完整修正记录）
1. FeatherPen/config.yaml：拆分web/llm独立配置节点，固化默认端口6554/1234，新增.env覆盖注释
2. FeatherPen/src/config/config_loader.py：删除load_config，新增端口非法值兜底、环境变量解析逻辑
3. FeatherPen/src/database/db_sqlite.py：导入名称load_config修正为load_global_config，废弃db_get_user_info
4. FeatherPen/src/database/init_db.py：新增数据库一键初始化脚本，目录树补充归档
5. FeatherPen/main.py：修正导入顺序，先加载配置函数再实例化cfg对象
6. FeatherPen/web/assets/js/api_client.js：删除硬编码端口描述，统一动态读取规范
7. FeatherPen/init_env.py：补全小说工程四级目录自动创建逻辑
8. 目录树补全data/Book/自定义书名四级子目录、dist多平台打包文件清单
9. docs/API_MODULE_SPEC.md：同步更新废弃黑名单、端口链路、数据库表完整字段
10. 全项目检索清理8位UID、旧函数名残留代码
11 两份文档统一新增自动初始化机制完整说明

## 第六部分 分层架构国标说明（补全遗漏章节）
1. 后端业务层：src（账号、数据库、AI生成）
2. 前端视图层：web（纯静态HTML，无后端混写）
3. 归档文档层：docs（全部国标规范文档）
4. 测试质量层：tests（单元/压力测试）
5. 运行支撑层：runtime（日志、缓存、临时文件）
6. 持久存储层：data（账号库、小说工程）
7. 静态资源层：assets（字体、图标、前端库）
8. 产物发布层：dist（各平台安装包）

## 第七部分 自动初始化完整规范（补全遗漏）
1. init_env.py：缺失data/runtime全套目录自动递归生成
2. init_db.py + db_sqlite.py：featherpen.db缺失自动执行sql_init.sql建十级账号
3. config.yaml缺失自动写入6554/1234国标端口配置
4. 小说工程目录缺失自动创建db/chapters/vector/snapshot四级文件夹