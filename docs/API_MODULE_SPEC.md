# FeatherPen/docs/API_MODULE_SPEC.md
<!-- GB/T 8567-2006 软件模块、端口、接口统一基准文档 -->
# 硬性同步规则：修改端口/函数/接口/文件，必须同步更新本文 + STRUCTURE.md
# 约束：仅国标业务注释，删除所有调试、草稿、临时内容

# 第一部分 File Path_世界树完整三级文件结构树（与STRUCTURE.md完全一致）
FeatherPen/
├── .gitignore                          # Git忽略配置，屏蔽日志、缓存、打包、临时文件
├── LICENSE                             # MIT开源协议文本
├── pyproject.toml                      # Python构建配置，移除Electron/PyQt6依赖
├── requirements.txt                    # 生产依赖：uvicorn/fastapi/pywebview/pycryptodome
├── requirements-dev.txt                # 开发单元测试依赖清单
├── init_env.py                         # 环境初始化，自动创建四级目录，缺失配置写入6554/1234端口
├── main.py                             # 程序顶层启动入口，加载配置启动双服务
├── .github/
│   └── workflows/
│       └── ci_build.yml                # 跨平台CI打包流水线
├── docs/
│   ├── README.md                       # 项目快速上手文档
│   ├── CHANGELOG.md                    # 版本迭代日志
│   ├── STRUCTURE.md                    # 主架构归档文档
│   ├── API.md                          # HTTP接口详细手册
│   ├── API_MODULE_SPEC.md              # 本基准规范文档
│   ├── COMPATIBILITY.md                # 跨平台兼容规范
│   ├── CONFIG_AND_API_SPEC.md          # 端口通信国标细则
│   ├── DATABASE_SCHEMA.md              # SQLite表结构规范
│   ├── DEPLOYMENT_GUIDE.md             # 打包部署指南
│   ├── PROJECT_OVERVIEW.md             # 项目离线隐私说明
│   ├── ACCOUNT_SPEC.md                 # Lv0-Lv9三层账号校验
│   ├── YESAPI_ACCOUNT.md               # 云端账号预留文档(V1.0不实现)
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
│   │   └── http_server.py              # FastAPI服务，6554端口，基准/api/v1
│   ├── account/
│   │   ├── __init__.py
│   │   ├── local_login.py              # 127001/6位账号常量定义，无端口
│   │   ├── member_ctrl.py              # 会员权限、Lv9开关函数
│   │   └── point_system.py             # 积分扣减逻辑
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_loader.py            # 读取6554/1234，废弃load_config
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm_api.py                  # LLM 1234端口通信
│   │   ├── memory_filter.py            # 对话过滤，无端口
│   │   ├── role_extract.py             # 角色提取，无端口
│   │   ├── novel_auto_gen.py           # 小说生成依赖1234端口
│   │   ├── world_check.py              # 世界观校验，无端口
│   │   └── progress_monitor.py         # AI进度监控，无端口
│   ├── database/
│   │   ├── __init__.py                 # 导出get_db_conn/get_account_info
│   │   ├── init_db.py                  # 数据库一键初始化
│   │   ├── db_sqlite.py                # SQLite账号查询，废弃db_get_user_info
│   │   ├── monitor_db.py               # 监控日志入库
│   │   └── sql_init.sql                # 建表+十级账号脚本
│   └── utils/
│       ├── __init__.py
│       ├── monitor/
│       │   ├── monitor_scheduler.py    # 定时监控
│       │   └── log_writer.py           # 日志脱敏
│       ├── process/                    # 子进程工具
│       └── i18n/                       # 多语言工具
├── web/
│   ├── index.html                      # 登录页，调用6554登录接口
│   ├── assets/
│   │   ├── css/main.css                # 全局样式
│   │   ├── js/api_client.js            # 动态读取Web端口，禁止硬编码
│   │   └── i18n/                       # 多语言文本
│   ├── pages/
│   │   ├── login.html                  # 独立登录页
│   │   ├── workbench.html              # 双端口6554/1234调用
│   │   ├── member.html                 # 会员面板
│   │   ├── model_setting.html          # 1234端口可视化配置
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
│   ├── FeatherPen_V1.0.0_Chrome_Plugin.zip
│   └── FeatherPen_V1.0.0_VSCode_Plugin.zip
├── config.yaml                         # 端口唯一配置源6554/1234
├── member_config.json                  # 6位特权账号配置
├── .env.example                        # FP_NETWORK_PREFERRED_PORT=6554
├── build.bat
└── setup.bat

# 第二部分 全文件【端口/函数/接口】完整明细（补全环境变量、数据库字段、页面调用）
## 1. FeatherPen/config.yaml
端口信息：
network.preferred_port=6554（Web前端API服务端口）
llm.local_api_port=1234（本地LM Studio推理端口）
绑定IP：127.0.0.1
环境变量覆盖键：FP_NETWORK_PREFERRED_PORT
冲突容错：启动检测端口占用，自动分配空闲端口
读取文件：src/config/config_loader.py、src/server/http_server.py、src/core/llm_api.py、web/assets/js/api_client.js
无导出函数，无HTTP接口

## 2. FeatherPen/src/config/config_loader.py
关联端口：6554、1234
导出标准函数：load_global_config()、load_member_config()、save_member_config()
废弃函数：load（永久禁用）
功能：解析yaml+环境变量，端口非法值自动回落默认

## 3. FeatherPen/src/server/http_server.py
占用端口：6554
监听地址：127.0.0.1
基准路由：/api/v1
标准HTTP接口：GET /api/v1/status、POST /api/v1/user/login
导出函数：run_server()

## 4. FeatherPen/src/database/db_sqlite.py
无网络端口
导出函数：get_db_conn()、get_account_info()
废弃函数：db_get_user_info（永久禁用）
依赖导入：load_global_config()
配套sql_init.sql完整数据表：local_user、sign_record、book_project、monitor_log

## 5. FeatherPen/src/core/llm_api.py
通信端口：1234
请求地址：http://127.0.0.1:{llm.local_api_port}/v1/chat/completions
导出函数：llm_client.generate_text()

## 6. FeatherPen/web/assets/js/api_client.js
前端请求统一前缀：http://127.0.0.1:{web_port}/api/v1
端口获取方式：页面初始化调用GET /api/v1/status动态拉取，禁止硬编码6554

## 7. 前端页面与接口对应关系（新增补全）
1. index.html / login.html → POST /api/v1/user/login（6554）
2. workbench.html → POST /api/v1/user/login + LLM 1234生成接口
3. model_setting.html → GET/PUT端口配置接口（6554）
4. monitor.html → GET /api/monitor/hardware（6554）

# 第三部分 HTTP接口全局统一规范（完整请求返回示例）
## 固定API基准前缀：/api/v1
### GET /api/v1/status
入参：无
返回结构：
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
### POST /api/v1/user/login
请求Content-Type: application/json
请求体：{"uid":"字符串","password":"字符串"}
成功返回data：{"uid":"","level":0~9,"point":999999999,"is_lv9":bool}
统一错误码：200成功、400参数错、401账号密码错、403权限不足、500服务异常

# 第四部分 三层账号校验常量（前后端完全对齐）
## Python src/account/local_login.py
OFFLINE_GUEST_UID = "127001"
PRIVILEGE_UID_LIST = ["000000","111111","222222","333333","444444","555555","666666","777777","888888","999999"]
## 前端JS全局常量（api_client.js）完全复制以上内容，禁止单独定义

# 第五部分 SQLite数据库完整字段规范（补全遗漏）
数据库路径：FeatherPen/data/database/featherpen
主表 local_user 字段清单
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
自动初始化：程序启动执行sql_init.sql插入000000~999999十级账号

# 第六部分 全局命名强制规则
1. 函数：snake_case；常量全大写；类PascalCase
2. 私有函数单下划线_开头，导出写入模块__all__
3. HTTP方法严格区分：GET查询、POST提交、PUT修改、DELETE删除

# 第七部分 全局废弃黑名单（两份文档同步）
废弃函数：load_config、db_get_user_info、SQLiteDB类
废弃业务：8位UID全套校验逻辑
废弃硬编码：代码直接写6554/1234数字
废弃目录：ui/、electron

# 第八部分 端口容错与初始化完整规范（新增补全）
1. 端口占用处理：http_server捕获OSError，随机分配空闲端口打印日志
2. 配置缺失兜底：init_env自动写入6554/1234默认yaml配置
3. 数据库缺失：init_db/db_sqlite自动执行sql_init.sql建表
4. 目录缺失：init_env递归创建data/runtime全套四级目录

# 第九部分 文档同步强制流程
1. 修改端口/函数/接口 → 同步更新本文 + STRUCTURE.md
2. 新增三级文件 → 两份文档同时补充File Path树条目
3. 废弃内容同步录入黑名单
4. 交付前核对目录树、端口、函数名三处完全一致