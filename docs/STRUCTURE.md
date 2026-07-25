# FeatherPen/docs/STRUCTURE.md
# FeatherPen V1.0.0 STRUCTURE文件结构树标准仓库完整目录架构文档
# 排序规则：文件夹优先按字母升序，同层级文件按英文字母升序排列
# 注释规范：# 后为文件/文件夹标准化业务说明，强制约束加粗标注
# 文档基准优先级：本目录规范 > 全平台兼容性规范 > 初代开发规范文档
# 架构变更说明：永久移除ui/PyQt6、electron目录，统一采用web/原生HTML + PyWebView桌面壳架构
# GB/T 8567-2006 软件文档编制规范配套归档文件
# 同步规则：所有新增/修改/删除文件，必须完整录入本文档；代码改动同步更新开发文档，文件与文档全程可追溯

# FeatherPen V1.0.0 世界树三级架构归档文档 GB/T 8567
# 排序规则：文件夹字母优先，同层级文件升序
# 变更同步规则：任何三级文件新增/修改/删除必须录入下方变更清单
# 废弃目录：ui/、electron/永久移除，统一web+PyWebView架构
# 全局约束：一级、二级目录不可修改，仅三级拓展

## 完整项目树形结构
FeatherPen/
├── .gitignore                     # Git忽略缓存、虚拟环境、打包产物
├── LICENSE                        # 开源协议文本
├── pyproject.toml                 # Python标准化构建配置
├── requirements.txt              # 生产运行依赖
├── requirements-dev.txt           # 开发测试依赖
├── init_env.py                    # 跨平台离线目录初始化、虚拟环境创建
├── main.py                        # 全局唯一启动入口：FastAPI子线程+PyWebView桌面
├── .github/workflows/ci_build.yml # CI全平台打包自动化脚本
├── docs/
│   ├── README.md                  # 项目快速上手文档
│   ├── CHANGELOG.md               # 版本迭代记录
│   ├── STRUCTURE.md               # 本文件，全项目文件追溯基准
│   ├── DEVELOP.md                 # 本地开发部署指南
│   ├── API.md                     # 后端离线全部接口规范
│   ├── COMPATIBILITY.md           # 多平台适配规范
│   ├── CONTRIBUTION.md            # 开发协作规范
│   ├── TEMPLATE.md                # 配置参数模板说明
│   ├── YESAPI_ACCOUNT.md          # V2云端账号预留文档
│   ├── WORLD_TREE.md              # 小说五级创作架构规范
│   └── PRESS_TEST.md              # Lv9亿级压测操作规范
├── src/
│   ├── __init__.py                # FastAPI后端根路由、接口注册
│   ├── account/
│   │   ├── __init__.py            # 账号模块导出
│   │   ├── local_login.py         # 账号前后端双层国标正则校验
│   │   ├── member_ctrl.py         # Lv9积分豁免开关持久化控制
│   │   └── point_system.py        # 积分扣费逻辑，区分特权豁免
│   ├── config/
│   │   ├── __init__.py            # 配置模块导出
│   │   └── config_loader.py       # yaml/json分层加载，非法参数回滚默认
│   ├── core/
│   │   ├── __init__.py            # AI核心引擎统一导出
│   │   ├── llm_api.py             # 本地LM Studio统一接口封装
│   │   ├── memory_filter.py       # 上下文章节过滤，控制投喂上限
│   │   ├── role_extract.py        # 小说角色自动提取归档
│   │   ├── novel_auto_gen.py      # 批量章节生成，50节自动校正
│   │   ├── world_check.py         # 世界观/时间线一致性校验
│   │   └── progress_monitor.py    # AI生成进度独立监控线程
│   ├── database/
│   │   ├── __init__.py            # 数据库模块导出
│   │   ├── db_sqlite.py           # SQLite AES加密CRUD封装
│   │   ├── init_db.py             # 程序启动自动执行建表SQL
│   │   ├── monitor_db.py          # 监控数据持久化存储
│   │   └── sql_init.sql           # 本地用户表、索引初始化脚本
│   └── utils/
│       ├── __init__.py            # 工具库导出
│       ├── monitor/
│       │   ├── __init__.py
│       │   ├── monitor_scheduler.py # 监控双线程调度
│       │   └── log_writer.py      # 日志7天自动清理、脱敏输出
│       ├── process/
│       └── i18n/                   # 多语言加载工具
├── web/
│   ├── index.html                 # 首页登录前端实时校验
│   ├── assets/
│   │   ├── css/main.css           # 全局页面样式
│   │   ├── js/api_client.js       # 前端SSE/HTTP请求封装
│   │   └── i18n/zh-CN.json/en-US.json # 多语言文案
│   ├── pages/
│   │   ├── login.html             # 独立登录页面输入校验
│   │   ├── workbench.html         # 小说创作工作台
│   │   ├── member.html            # Lv9积分豁免面板
│   │   ├── model_setting.html     # 本地模型参数配置页
│   │   ├── monitor.html           # 硬件+Token监控面板
│   │   └── snapshot_export.html   # 工程快照导出页面
│   └── public/file_handler.js     # 本地文件读写工具JS
├── tests/
│   ├── __init__.py
│   ├── account/                   # 账号模块单元测试
│   └── core/pressure/             # 批量生成压测用例
├── runtime/
│   ├── logs/                      # 分级日志目录
│   │   ├── monitor_log/monitor.log
│   │   ├── runtime_log/runtime.log
│   │   └── token_flow_log/token_flow.log
│   ├── cache/                     # 冷热文本缓存
│   └── temp/                      # 临时章节缓存
├── data/
│   ├── Book/
│   │   ├── User/127001/user_setting.json # Lv0离线游客配置
│   │   └──【自定义书名】/db/chapters/vector/snapshot # 单小说隔离工程
│   └── database/featherpen.db     # 加密本地数据库
├── assets/
│   ├── lib/多语言json
│   ├── fonts/
│   └── images/
└── dist/ # 各平台打包产物（自动生成）

# Feather 国标项目架构规范（GB/T 8567-2006）
## 一、架构总则
1. 项目**一、二级目录永久锁定**，禁止修改、新增、删除、重命名
2. 仅支持三级及以下目录合规业务拓展，所有迭代仅新增三级文件/子目录
3. 模块分层解耦：静态资源层、后端业务层、前端展示层、数据持久层、测试层、打包层完全隔离
4. 全文件统一编码：UTF-8无BOM；所有读写文件强制指定encoding="utf-8"
5. 代码约束：仅保留标准业务注释，删除调试、临时、废弃、重复冗余代码；所有函数/类配套国标规范注释
6. 文档同步约束：任意文件新增/修改/删除，必须同步更新本文STRUCTURE.md；代码逻辑改动同步更新docs内开发归档文档，无文档则交付无效

## 二、固定一级目录职责
- src：核心业务层（AI引擎、账号、数据库、工具）
- web：前端视图层（纯HTML桌面页面）
- docs：归档追溯层（国标规范、接口、结构、开发文档）
- tests：质量校验层（单元/压测用例）
- runtime：运行支撑层（日志、缓存、临时文件）
- data：持久存储层（用户小说、账号数据库）
- assets：全局资源层（多语言、字体、图片）
- dist：发布产物层（各平台离线安装包）
- .github：CI自动化流水线层

## 三、世界树五级国标创作层级（优先级自上而下不可逆）
1. 世界树总纲：全局最高世界观、核心设定（永久锁定）
2. 卷大纲：单卷主线、冲突、登场角色边界
3. 章大纲：单章叙事目标、伏笔、时间节点
4. 小节提纲：单节轻量化写作框架
5. 小节正文：最终生成文本，积分唯一扣费单元

## 四、数据存储国标规范
1. SQLite：仅存储账号、人设、大纲、统计等结构化元数据
2. 外置TXT：所有小说小节正文独立分文件存储，适配亿级字数低占用运行
3. 数据隔离：结构化库与大文本文件物理分离，避免数据库膨胀卡顿

## 五、三级拓展强制规范
1. 新增功能/模块仅允许在现有二级目录内新建三级文件/三级子文件夹
2. 禁止在一级、二级目录直接新增业务代码文件
3. 新增文件必须同步录入本文档：完整FeatherPen/开头路径 + 标准化功能注释
4. 废弃文件需在本文档标注废弃说明，保留归档记录不删除条目

# 核心文件功能注释信息

### FeatherPen/src/database/sql_init.sql
- **功能描述**：SQLite 数据库初始化核心脚本。
- **规范要求**：遵循 GB/T 8567-2006 规范。负责全自动建表、业务索引构建及十级离线管理员账号初始化。涵盖本地离线用户主表、多凭证绑定表、独立积分资产表、**用户会员订单流水表（支持多等级叠加与平滑降级）**、小说工程隔离表、五级世界章节小节表及五维(TOK→GEN→CPU→GPU→MEM)监控日志表。

# 全量代码更新归档条目
FeatherPen/main.py | 删除废弃PyQt6双启动冗余代码，统一UTF8规范注释，修复路径拼接BUG
FeatherPen/init_env.py | 清理临时调试打印，标准化跨平台目录创建逻辑，统一文件读写编码
FeatherPen/config.yaml | 对齐开发文档账号、积分、模型全部国标参数规范
FeatherPen/member_config.json | 统一特权账号为6位UID，每条配置追加账号输入规范注释
FeatherPen/src/__init__.py | 新增账号查重离线接口，统一所有接口标准化返回格式
FeatherPen/src/account/local_login.py | 实现文档规定账号/密码前后端双层正则校验，兼容主板自动登录逻辑
FeatherPen/src/config/config_loader.py | 删除重复两套Config类冗余代码，重构标准单例模式，修复配置读取报错
FeatherPen/docs/STRUCTURE.md | 同步本次全量代码修改、新增文件，完整三级路径+标准化功能注释录入，融合完整目录树与国标架构规范
FeatherPen/docs/FeatherPen（羽笔）V1.0.0 开发文档.docx | 同步更新账号校验、数据库唯一索引、前后端双层校验全套规范章节

## 本次代码修正归档清单（同步本次所有修改）
1. FeatherPen/init_env.py | 清理废弃打印，标准化目录创建，固定离线游客127001路径
2. FeatherPen/main.py | 删除PyQt6冗余双启动代码，标准化线程服务逻辑
3. FeatherPen/config.yaml | 固化TCP网络、离线UID国标参数，删除重复配置段
4. FeatherPen/member_config.json | 统一Lv0~Lv9权限积分，规范账号注释
5. FeatherPen/src/account/local_login.py | 前后端对齐正则，豁免账号逻辑简化，删除重复校验函数
6. FeatherPen/src/config/config_loader.py | 移除重复配置类，单例标准化分层加载
7. FeatherPen/src/database/sql_init.sql | 完善唯一索引，注释国标字段约束
8. FeatherPen/web/index.html | 精简JS校验代码，删除冗余提示文案
9. FeatherPen/web/pages/login.html | 复用统一校验逻辑，移除重复正则定义
10. FeatherPen/src/database/init_db.py | 清理调试输出，兼容旧数据库升级字段
