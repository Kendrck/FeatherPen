# FeatherPen/docs/API_MODULE_SPEC.md
<!-- GB/T 8567-2006 软件模块、端口、接口统一基准文档 -->
# 硬性同步规则：修改端口/函数/接口/文件，必须同步更新本文 + docs/STRUCTURE.md
# 约束：仅国标业务注释，删除调试/草稿/临时废弃内容，零冗余

# 第一部分 File Path_世界树完整三级文件结构树
FeatherPen/
├── .gitignore                          # Git忽略配置，屏蔽日志缓存打包临时文件
├── LICENSE                             # MIT开源协议文本
├── pyproject.toml                      # Python构建配置，移除Electron/PyQt6依赖
├── requirements.txt                    # 生产依赖：uvicorn/fastapi/pywebview/pycryptodome
├── requirements-dev.txt                # 开发单元测试依赖清单
├── init_env.py                         # 环境初始化，自动创建四级目录，缺失config写入6554/1234端口
├── main.py                             # 程序顶层启动入口，加载配置启动双服务
├── .github/
│   └── workflows/
│       └── ci_build.yml                # 跨平台CI打包流水线
├── docs/
│   ├── README.md                       # 项目快速上手文档
│   ├── CHANGELOG.md                    # 版本迭代日志
│   ├── STRUCTURE.md                    # 主架构归档文档
│   ├── API_MODULE_SPEC.md              # 本基准规范文档
│   ├── API.md                          # HTTP接口完整手册
│   ├── COMPATIBILITY.md                # 跨平台兼容规范
│   ├── CONFIG_AND_API_SPEC.md          # 端口通信国标细则
│   ├── DATABASE_SCHEMA.md              # SQLite表结构规范
│   ├── DEPLOYMENT_GUIDE.md             # 打包部署指南
│   ├── PROJECT_OVERVIEW.md             # 项目离线隐私说明
│   ├── ACCOUNT_SPEC.md                 # Lv0-Lv9三层离线账号校验
│   ├── DEVELOP.md                      # 开发调试指南
│   ├── PRESS_TEST.md                   # Lv9压测解锁规范
│   ├── local_member_config_v1.0.0.json # 会员配置模板
│   ├── dev/
│   │   ├── Project_Structure.md        # 开发目录解读
│   │   ├── UI_Compatibility_Spec.md    # Web前端兼容规范
│   │   ├── Code_Style.md               # 编码注释国标
│   │   ├── Test_Guide.md               # 单元测试规范
│   │   └── Build_Guide.md              # Windows打包脚本说明
│   ├── user/
│   │   ├── Install_Guide.md            # 用户安装教程
│   │   ├── Language_Spec.md            # i18n多语言规范
│   │   ├── Data_Import_Export.md       # 小说工程导入导出
│   │   └── FAQ.md                      # 端口/登录报错解决方案
│   └── assets/                         # 文档配图资源
├── src/
│   ├── __init__.py                     # 后端根包导出
│   ├── server/
│   │   └── http_server.py              # FastAPI服务，端口6554，基准/api/v1
│   ├── account/
│   │   ├── __init__.py
│   │   ├── local_login.py              # 127001/6位特权账号常量，无端口
│   │   ├── member_ctrl.py              # 会员等级、Lv9积分开关函数
│   │   └── point_system.py             # 积分扣减逻辑
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_loader.py            # 读取6554/1234，废弃load_config
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm_api.py                  # LLM通信端口1234
│   │   ├── memory_filter.py            # 对话过滤，无端口
│   │   ├── role_extract.py             # 角色提取，无端口
│   │   ├── novel_auto_gen.py           # 生成依赖1234端口
│   │   ├── world_check.py              # 世界观校验，无端口
│   │   └── progress_monitor.py         # AI进度监控，无端口
│   ├── database/
│   │   ├── __init__.py                 # 导出get_db_conn、get_account_info
│   │   ├── init_db.py                  # 数据库一键初始化
│   │   ├── db_sqlite.py                # SQLite账号查询，废弃db_get_user_info
│   │   ├── monitor_db.py               # 监控日志入库
│   │   └── sql_init.sql                # 建表+6位十级账号脚本
│   └── utils/
│       ├── __init__.py
│       ├── monitor/
│       │   ├── monitor_scheduler.py    # 定时监控
│       │   └── log_writer.py           # 日志脱敏
│       ├── process/                    # 子进程工具
│       └── i18n/                       # 多语言工具
├── web/
│   ├── index.html                      # 登录页，依赖6554登录接口
│   ├── assets/
│   │   ├── css/main.css                # 全局样式
│   │   ├── js/api_client.js            # 动态获取端口，禁止硬编码
│   │   └── i18n/                       # 多语言文本
│   ├── pages/
│   │   ├── login.html                  # 独立登录页
│   │   ├── workbench.html              # 双端口6554/1234
│   │   ├── member.html                 # 会员面板
│   │   ├── model_setting.html          # LLM 1234端口配置
│   │   ├── monitor.html                # AI监控面板
│   │   └── snapshot_export.html        # 快照导出
│   └── public/
│       └── file_handler.js             # 文件读写JS
├── tests/
│   ├── __init__.py
│   ├── account/                        # 账号单元测试
│   └── core/pressure/                  # Lv9压测用例
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
│   │   └──【自定义书名】/
│   │       ├── db/
│   │       ├── chapters/
│   │       ├── vector/
│   │       └── snapshot/
│   └── database/
├── assets/
│   ├── lib/
│   ├── fonts/
│   └── images/
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
├── config.yaml                         # 端口唯一配置源6554/1234
├── member_config.json                  # 6位本地特权账号配置
├── .env.example                        # FP_NETWORK_PREFERRED_PORT=6554
├── build.bat
└── setup.bat

# 第二部分 全文件【端口/函数/接口】完整明细
## 1 FeatherPen/config.yaml
端口定义：
network.preferred_port=6554（Web服务）
llm.local_api_port=1234（本地推理）
绑定地址：127.0.0.1
环境变量覆盖键：FP_NETWORK_PREFERRED_PORT
容错：端口占用自动分配空闲端口
读取文件：src/config/config_loader.py、src/server/http_server.py、src/core/llm_api.py、web/assets/js/api_client.js

## 2 FeatherPen/src/config/config_loader.py
关联端口：6554、1234
标准导出函数：load_global_config()、load_member_config()、save_member_config()
废弃函数：load_config（永久禁用）

## 3 FeatherPen/src/server/http_server.py
占用端口：6554，监听127.0.0.1
基准路由前缀 /api/v1
标准HTTP接口：GET /api/v1/status、POST /api/v1/user/login
导出函数：run_server()

## 4 FeatherPen/src/core/llm_api.py
通信端口1234
请求基准地址：http://127.0.0.1:{llm.local_api_port}/v1/chat/completions
导出函数：llm_client.generate_text()

## 5 FeatherPen/web/assets/js/api_client.js
请求统一前缀：http://127.0.0.1:{web_port}/api/v1
端口获取方式：页面初始化调用/api/v1/status动态拉取，禁止硬编码数字

## 6 前端页面与接口对应关系
index.html / login.html → POST /api/v1/user/login（6554）
workbench.html → 6554后端 + 1234模型双调用
model_setting.html → 6554配置接口修改1234端口

# 第三部分 HTTP接口全局统一规范
固定API基准前缀：/api/v1
## GET /api/v1/status
{
  "code": 200,
  "detail": "服务正常运行",
  "data": {
    "service_name": "FeatherPen",
    "version": "V1.0.0",
    "offline_uid": "127001",
    "web_port": 6554
  }
}
## POST /api/v1/user/login
请求Content-Type: application/json
请求体 {"uid":"字符串","password":"字符串"}
成功返回data：{"uid":"","level":0~9,"point":999999999,"is_lv9":bool}
全局错误码：200成功、400参数非法、401账号错误、403权限不足、500服务异常

# 第四部分 三层离线账号全局常量（前后端完全对齐）
## Python src/account/local_login.py
OFFLINE_GUEST_UID = "127001"
PRIVILEGE_UID_LIST = ["000000","111111","222222","333333","444444","555555","666666","777777","888888","999999"]
## 前端api_client.js 完全复制以上常量，禁止单独自定义

# 第五部分 SQLite数据库标准规范
数据库路径：FeatherPen/data/database/featherpen.db
主表 local 完整字段：
uid CHAR(64) PRIMARY KEY
level TINYINT DEFAULT 0
password VARCHAR(128) NOT NULL
point BIGINT DEFAULT 999999999
bind_email VARCHAR(64) NULL
bind_phone VARCHAR(20) NULL
desc_text VARCHAR(256) NULL
create_time DATETIME DEFAULT CURRENT_TIMESTAMP
last_login_time DATETIME NULL
status TINYINT DEFAULT 1
初始化规则：sql_init.sql自动创建表，插入000000~999999十级6位账号，邮箱/手机号建立唯一索引

# 第六部分 Python/JS命名强制规则
1. 普通函数：snake_case；全局常量：全大写下划线；类：PascalCase
2. 单下划线_开头为内部私有函数，模块导出写入__all__
3. HTTP语义统一：GET查询、POST新增提交、PUT修改、DELETE删除

# 第七部分 全局废弃黑名单（全项目清理完毕）
废弃函数：load_config、db_get_user_info、SQLiteDB类
废弃业务：8位UID、YesApi云端登录、cloud_login接口
废弃硬编码：代码直接书写6554/1234
废弃目录：ui/、electron
废弃文档：docs/YESAPI_ACCOUNT.md（物理删除）

# 第八部分 端口与自动初始化完整规范
1. 端口冲突捕获OSError，自动分配空闲端口并打印日志
2. config.yaml缺失自动写入6554/1234国标默认配置
3. 数据库文件/数据表缺失自动执行sql_init.sql建表插账号
4. data/Book小说目录缺失自动生成db/chapters/vector/snapshot四级子目录

# 第九部分 文档同步强制流程
1. 修改端口/函数/接口 → 同步更新本文 + STRUCTURE.md
2. 新增/删除三级文件 → 两份文档同步补充/移除目录树条目
3. 废弃内容统一录入黑名单，全项目检索清理所有调用
4. 交付校验：目录树、端口参数、函数名称三者完全一致无冲突