# FeatherPen/docs/API_MODULE_SPEC.md
# GB/T 8567 V1.0.0 软件模块、端口、接口统一基准文档
# 同步强制规则：修改端口/函数/接口/文件，同步更新本文 + docs/STRUCTURE.md
# 约束：仅国标业务注释，删除调试、草稿、临时冗余内容，零冗余
# 第一部分 File Path_世界树完整三级文件结构树
FeatherPen/
├── .gitignore                          # Git忽略配置，过滤日志、缓存、打包临时文件
├── LICENSE                             # MIT开源许可文本
├── pyproject.toml                      # Python构建配置，移除Electron/PyQt6依赖
├── requirements.txt                    # 生产依赖：uvicorn/fastapi/pywebview/pycryptodome
├── requirements-dev.txt                # 单元测试开发依赖清单
├── init_env.py                         # 环境初始化，自动创建四级目录，写入6554/1234端口
├── main.py                             # 程序顶层启动入口
├── .github/
│   └── workflows/
│       └── ci_build.yml                # CI跨平台自动打包流水线
├── docs/
│   ├── README.md                       # 项目快速上手总览
│   ├── CHANGELOG.md                    # 版本变更归档日志
│   ├── STRUCTURE.md                    # 三级架构主归档文档
│   ├── API_MODULE_SPEC.md              # 本文档，端口/函数基准
│   ├── API.md                          # HTTP完整接口手册
│   ├── COMPATIBILITY.md                # 多系统兼容国标
│   ├── CONFIG_AND_API_SPEC.md          # 端口通信配置细则
│   ├── DATABASE_SCHEMA.md              # SQLite数据表规范
│   ├── DEPLOYMENT_GUIDE.md             # 打包部署指南
│   ├── PROJECT_OVERVIEW.md             # 离线隐私整体规范
│   ├── ACCOUNT_SPEC.md                 # 账号三层校验国标
│   ├── DEVELOP.md                      # 开发调试规范
│   ├── PRESS_TEST.md                   # 特权UID白名单压测规范
│   ├── local_member_config_v1.0.0.json # 会员权限模板
│   ├── dev/
│   │   ├── Project_Structure.md        # 开发目录解读
│   │   ├── UI_Compatibility_Spec.md    # Web前端兼容规范
│   │   ├── Code_Style.md               # 编码注释国标
│   │   ├── Test_Guide.md               # 单元测试规范
│   │   └── Build_Guide.md              # Windows打包说明
│   ├── user/
│   │   ├── Install_Guide.md            # 用户安装教程
│   │   ├── Language_Spec.md            # 多语言规范
│   │   ├── Data_Import_Export.md       # 工程导入导出规范
│   │   └── FAQ.md                      # 报错解决方案
│   └── assets/                         # 文档配图资源
├── src/
│   ├── __init__.py                     # 后端根包导出入口
│   ├── server/
│   │   └── http_server.py              # FastAPI Web服务，默认6554，基准/api/v1
│   ├── account/
│   │   ├── __init__.py
│   │   ├── local_login.py              # 游客、特权UID白名单常量、账号正则
│   │   ├── member_ctrl.py              # 权限判定唯一依据为白名单，Lv9无积分/压测特权
│   │   └── point_system.py             # 积分扣减，白名单UID自动豁免
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_loader.py            # 读取yaml/env端口，废弃load_config
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm_api.py                  # LLM推理端口固定1234
│   │   ├── memory_filter.py            # 对话上下文过滤
│   │   ├── role_extract.py             # 人物提取模块
│   │   ├── novel_auto_gen.py           # AI章节生成，依赖1234、白名单积分判定
│   │   ├── world_check.py              # 世界观校验
│   │   └── progress_monitor.py         # AI生成进度监控
│   ├── database/
│   │   ├── __init__.py
│   │   ├── init_db.py                  # 数据库初始化
│   │   ├── db_sqlite.py                # 账号CRUD，废弃db_get_user_info
│   │   ├── monitor_db.py               # 监控日志入库
│   │   └── sql_init.sql                # 建表+预置10组特权UID白名单账号
│   └── utils/
│       ├── __init__.py
│       ├── monitor/
│       │   ├── monitor_scheduler.py    # 硬件监控定时
│       │   └── log_writer.py           # 日志脱敏工具
│       ├── process/                    # 跨平台子进程工具
│       └── i18n/                       # 全局多语言工具
├── web/
│   ├── index.html                      # 登录首页
│   ├── assets/
│   │   ├── css/main.css                # 全局前端样式
│   │   ├── js/api_client.js            # 动态拉取端口，前后端常量完全对齐
│   │   └── i18n/                       # 多语言文本资源
│   ├── pages/
│   │   ├── login.html                  # 独立登录页面
│   │   ├── workbench.html              # 6554/1234双端口工作台
│   │   ├── member.html                 # 特权开关面板
│   │   ├── model_setting.html          # LLM端口配置页
│   │   ├── monitor.html                # AI监控面板
│   │   └── snapshot_export.html        # 快照导出页面
│   └── public/
│       └── file_handler.js             # 前端本地文件读写JS
├── tests/
│   ├── __init__.py
│   ├── account/                        # 账号权限单元测试
│   └── core/pressure/                  # 压测专项测试用例
├── runtime/
│   ├── logs/
│   │   ├── monitor_log/monitor.log
│   │   ├── runtime_log/runtime.log
│   │   └── token_flow_log/token_flow.log
│   ├── cache/
│   └── temp/
├── data/
│   ├── Book/
│   │   ├── User/127001/
│   │   └──【自定义书名】/db/chapters/vector/snapshot
│   └── database/featherpen.db
├── assets/
│   ├── lib/
│   ├── fonts/
│   └── images/
├── dist/各类平台打包产物
├── config.yaml                         # Web6554 LLM1234端口配置源
├── member_config.json                  # 特权UID白名单配置
├── .env.example                        # 端口环境变量模板
├── build.bat / setup.bat
# 第二部分 全文件端口/函数/接口标准化明细
## 1 FeatherPen/config.yaml
文件路径：FeatherPen/config.yaml
端口参数：
network.preferred_port 默认6554，占用自动分配空闲端口
llm.local_api_port 固定1234，无自动分配逻辑
绑定地址：127.0.0.1
环境变量：FP_NETWORK_PREFERRED_PORT（仅覆盖Web端口）
读取依赖：src/config/config_loader.py、src/server/http_server.py、src/core/llm_api.py、web/assets/js/api_client.js、web/pages/model_setting.html
## 2 FeatherPen/src/config/config_loader.py
文件路径：FeatherPen/src/config/config_loader.py
关联端口：6554、1234
导出函数：load_global_config() / load_member_config() / save_member_config()
废弃函数：load_config
## 3 FeatherPen/src/server/http_server.py
文件路径：FeatherPen/src/server/http_server.py
占用端口6554，监听127.0.0.1，基准/api/v1
导出函数run_server()
核心接口：GET /api/v1/status、POST /api/v1/user/login
## 4 FeatherPen/src/account/local_login.py
文件路径：FeatherPen/src/account/local_login.py
无端口依赖
全局强制常量（前后端完全一致）：
OFFLINE_GUEST_UID = "127001"
PRIVILEGE_UID_LIST = ["000000","111111","222222","333333","444444","555555","666666","777777","888888","999999"]
业务：账号格式校验、游客/白名单身份匹配
## 5 FeatherPen/src/account/member_ctrl.py
文件路径：FeatherPen/src/account/member_ctrl.py
无端口依赖
核心函数：
get_user_level(uid)：读取会员等级（仅控制章节生成上限）
is_privilege_uid(uid)：积分豁免、压测权限唯一判定条件
toggle_point_deduct_switch(uid)：仅白名单UID可调用，纯Lv9账号返回403
unlock_pressure_mode(uid)：仅白名单UID可调用
注释标准：Lv9仅扩容章节上限，无积分、压测专属特权
## 6 FeatherPen/src/account/point_system.py
文件路径：FeatherPen/src/account/point_system.py
无端口依赖
核心函数consume_point(uid, cost)
扣减逻辑：is_privilege_uid=true直接跳过扣费；纯Lv9标准账号正常扣费
## 7 FeatherPen/src/core/llm_api.py
文件路径：FeatherPen/src/core/llm_api.py
通信端口1234，推理地址固定模板，导出llm_client.generate_text()
## 8 FeatherPen/src/core/novel_auto_gen.py
文件路径：FeatherPen/src/core/novel_auto_gen.py
依赖端口1234，依赖point_system、member_ctrl，关联POST /api/v1/novel/gen_chapter
## 9 FeatherPen/web/assets/js/api_client.js
文件路径：FeatherPen/web/assets/js/api_client.js
基准地址 http://127.0.0.1:{web_port}/api/v1
端口动态从/status拉取，禁止硬编码；常量完整复制后端白名单列表
## 10 全局HTTP接口基准 /api/v1
### 系统基础
GET /api/v1/status：获取端口、版本、游客UID
### 用户账号模块
POST /api/v1/user/login：三层账号校验
GET /api/v1/user/check_name：注册查重
GET /api/v1/user/info：账号权限信息
POST /api/v1/user/register：新建本地账号
### 会员积分模块
GET /api/v1/member/level_config：读取全套等级参数
POST /api/v1/member/toggle_lv9_deduct：仅白名单账号可调用，非白名单返回403
### AI生成模块
POST /api/v1/novel/gen_chapter：白名单UID自动豁免积分扣费
POST /api/v1/novel/gen_role / gen_timeline / world_check
### 快照、监控、配置接口
GET /api/v1/snapshot/list
POST /api/v1/snapshot/export / import
GET /api/monitor/hardware / token_stat / progress
GET /api/config/network_info
## 11 统一错误码分层说明
200 请求成功
400 参数非法
401 账号密码校验失败
403 权限不足（等级不足 / 非特权UID白名单调用积分、压测接口）
500 服务内部异常
## 12 命名国标强制规则
Python：函数snake_case、类PascalCase、全局常量全大写
JS：函数camelCase、全局常量全大写
HTTP语义：GET查询、POST提交、PUT更新、DELETE删除
## 13 全局废弃黑名单（与STRUCTURE.md完全同步）
废弃函数：load_config、db_get_user_info、旧SQLiteDB类
废弃业务：8位UID、YesApi、cloud_login云端接口
废弃目录：ui/、electron，无导入无打包分支
废弃硬编码：直接书写6554/1234数字