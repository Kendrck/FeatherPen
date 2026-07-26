# FeatherPen/docs/dev/Project_Structure.md
# GB/T 8567-2006 项目分层架构标准文档 V1.0.0
## 文档约束
1. 一、二级目录固定不可增删改名，仅允许三级文件/子目录拓展
2. 所有新增、删除文件必须同步更新 STRUCTURE.md、API_MODULE_SPEC.md
3. 废弃目录 ui/、electron 永久不创建、无代码导入
4. 仅保留国标业务说明，删除草稿、迭代、临时规划文字

## 一、全局完整目录树（纯净标准化）
FeatherPen/
├── main.py                          # 程序唯一顶层启动入口
├── pyproject.toml                   # Python标准化构建配置
├── config.yaml                      # 全局端口/业务唯一配置源
├── .env.example                     # 环境变量端口覆盖模板
├── requirements.txt                 # 生产依赖清单
├── requirements-dev.txt             # 开发单元测试依赖
├── init_env.py                      # 全目录自动初始化脚本
├── .gitignore                       # Git忽略缓存/日志/打包文件
├── src/                             # 后端纯业务逻辑层
│   ├── __init__
│   ├── account/                     # 账号、会员、积分模块
│   │   ├── __init__.py
│   │   ├── local_login.py           # 127001游客+6位特权账号校验
│   │   ├── member_ctrl.py           # Lv0-Lv9权限控制
│   │   └── point_system.py          # 积分扣减统计
│   ├── config/                      # 全局配置加载模块
│   │   ├── __init__.py
│   │   └── config_loader.py         # 读取yaml/环境变量，标准函数load_global_config
│   ├── core/                        # AI小说生成核心引擎
│   │   ├── __init__.py
│   │   ├── llm_api.py               # LM Studio 1234推理端口通信
│   │   ├── memory_filter.py         # 对话上下文过滤
│   │   ├── role_extract.py          # 角色自动提取
│   │   ├── novel_auto_gen.py        # 章节批量生成
│   │   ├── world_check.py           # 世界观一致性校验
│   │   └── progress_monitor.py     # AI生成进度监控
│   ├── database/                    # SQLite持久层
│   │   ├── __init__.py
│   │   ├── init_db.py               # 数据库一键初始化
│   │   ├── db_sqlite.py             # 账号CRUD，标准函数get_account_info
│   │   ├── monitor_db.py           # 监控日志入库
│   │   └── sql_init.sql            # 十级账号建表脚本
│   └── utils/                       # 通用无业务工具库
│       ├── __init__.py
│       ├── monitor/                 # 硬件监控工具
│       ├── process/                 # 子进程调度
│       └── i18n/                    # 多语言翻译工具
├── web/                             # 纯静态前端视图层（PyWebView承载）
│   ├── index.html
│   ├── assets/css/main.css
│   ├── assets/js/api_client.js      # 统一请求封装，动态读取6554端口
│   ├── pages/                       # 登录/工作台/配置页面
│   └── public/file_handler.js
├── tests/                           # 单元测试分层目录
│   ├── account/
│   └── core/pressure/
├── docs/                            # 全套国标归档文档
│   ├── STRUCTURE.md
│   ├── API_MODULE_SPEC.md
│   ├── API.md
│   ├── ACCOUNT_SPEC.md
│   ├── CONFIG_AND_API_SPEC.md
│   ├── DATABASE_SCHEMA.md
│   ├── COMPATIBILITY.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── DEVELOP.md
│   ├── PRESS_TEST.md
│   ├── dev/                         # 开发细则文档（本文所在目录）
│   └── user/                        # 用户操作手册
├── data/                            # 本地持久小说工程、账号库
│   ├── database/featherpen.db
│   └── Book/【自定义书名】四级工程目录
├── runtime/                         # 运行日志、缓存、临时导出
├── assets/                          # 字体、UI图标、前端静态库
├── dist/                            # 各平台打包产物
├── build.bat / setup.bat            # Windows打包、初始化脚本

## 二、分层解耦强制规则
1. 后端src层：无UI交互代码，仅提供/api/v1接口
2. 前端web层：禁止直接读写数据库、配置文件，全部走HTTP接口
3. utils工具包：零业务耦合，仅提供通用能力
4. database层：仅本地SQLite，无云端远程连接逻辑
5. 端口规范：Web 6554 / LLM 1234，统一读取config_loader，禁止硬编码

## 三、模块依赖单向约束（禁止循环依赖）
1. ui/web → 仅依赖src/server HTTP接口，禁止直接导入src源码
2. src/core → 依赖config、database、utils，不依赖账号上层逻辑
3. src/account → 依赖config、database，不依赖AI生成模块
4. 所有模块统一通过config_loader读取全局配置

## 四、废弃目录永久约束
ui/、electron 两套旧图形界面目录永久废弃，源码、打包脚本不再创建对应文件夹，目录黑名单录入STRUCTURE.md、API_MODULE_SPEC.md。

## 五、文档同步规则
新增/删除三级文件，必须同步：
1. STRUCTURE.md File Path世界树
2. API_MODULE_SPEC.md 文件索引
3. 对应模块开发/用户文档补充注释说明