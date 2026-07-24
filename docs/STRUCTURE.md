# FeatherPen/docs/STRUCTURE.md
# FeatherPen V1.0.0 STRUCTURE文件结构树标准仓库完整目录架构文档
# 排序规则：文件夹优先按字母升序，同层级文件按英文字母升序排列
# 注释规范：# 后为文件/文件夹标准化业务说明，强制约束加粗标注
# 文档基准优先级：本目录规范 > 全平台兼容性规范 > 初代开发规范文档
# 架构变更说明：永久移除ui/PyQt6、electron目录，统一采用web/原生HTML + PyWebView桌面壳架构
# GB/T 8567-2006 软件文档编制规范配套归档文件
# 同步规则：所有新增/修改/删除文件，必须完整录入本文档；代码改动同步更新开发文档，文件与文档全程可追溯

FeatherPen/ # 项目根一级目录
├── .gitignore # Git版本忽略配置文件
├── LICENSE # 开源协议文本
├── pyproject.toml # Python标准化构建配置，移除Electron/PyQt6打包配置
├── requirements.txt # 生产环境依赖，新增pywebview，删除electron、PyQt6
├── requirements-dev.txt # 开发/单元测试依赖清单
├── init_env.py # 跨平台离线环境一键初始化脚本【根启动环境标准化脚本】
├── main.py # 全局唯一程序启动入口：异步启动FastAPI+拉起PyWebView桌面窗口【程序总入口】
├── .github/ # CI/CD自动化流水线根目录
│   └── workflows/ # CI工作流二级目录
│       └── ci_build.yml # 全平台离线打包脚本，产物输出至dist目录
├── docs/ # 国标归档文档库，所有文件变更同步STRUCTURE.md
│   ├── README.md # 项目快速上手文档，标注V1.0纯离线、在线功能V2.0预留
│   ├── CHANGELOG.md # 版本迭代日志，区分离线V1.0与云端V2.0规划
│   ├── STRUCTURE.md # 世界树目录追溯核心文档，全项目文件路径归档【本文档】
│   ├── DEVELOP.md # 本地离线开发部署指南
│   ├── API.md # 后端离线接口全集，云端接口仅注释预留
│   ├── COMPATIBILITY.md # 全平台适配与dist打包命名规范
│   ├── CONTRIBUTION.md # 开发者协作国标规范
│   ├── TEMPLATE.md # config/member_config配置模板说明
│   ├── YESAPI_ACCOUNT.md # V2.0云端对接预留文档，V1.0不开发代码
│   ├── WORLD_TREE.md # 小说五级世界树创作架构专项文档
│   ├── PRESS_TEST.md # Lv9离线亿级字数压测操作规范
│   └── FeatherPen（羽笔）V1.0.0 开发文档.docx # GB/T 8567完整国标归档文档
├── src/ # Python Core后端内核，FastAPI内置服务【后端核心二级目录，锁定不可增删】
│   ├── __init__.py # FastAPI后端服务入口，注册全部离线业务接口
│   ├── account/ # 离线本地账号模块，无云端交互
│   │   ├── __init__.py # 账号模块初始化导出
│   │   ├── local_login.py # 纯本地离线登录逻辑，国标账号/密码双层正则校验
│   │   ├── member_ctrl.py # Lv0~Lv9本地权限判定，Lv9积分豁免开关持久化
│   │   └── point_system.py # 本地积分扣费逻辑，全局固定积分999999999
│   ├── config/ # 全局配置加载模块
│   │   ├── __init__.py # 配置模块初始化导出
│   │   └── config_loader.py # yaml/json配置单例加载、非法参数自动回滚默认值，清理重复冗余代码
│   ├── core/ # AI长篇生成核心引擎
│   │   ├── __init__.py # 核心引擎初始化导出
│   │   ├── llm_api.py # 本地三模型SSE流式统一封装，无外网推理依赖
│   │   ├── memory_filter.py # 三层冷热本地记忆、Token截断处理
│   │   ├── role_extract.py # 小说角色自动提取、本地持久归档
│   │   ├── novel_auto_gen.py # 五级大纲生成、单章生成、每50章自动全局剧情校验
│   │   ├── world_check.py # 100节区间人设/时间线/伏笔统一校验
│   │   └── progress_monitor.py # AI生成进度、硬件监控独立守护线程
│   ├── database/ # SQLite本地加密持久层
│   │   ├── __init__.py # 数据库模块初始化导出
│   │   ├── db_sqlite.py # AES加密本地连接池、账号/小说元数据CRUD
│   │   ├── init_db.py # 程序启动自动建表脚本，含用户唯一索引
│   │   └── monitor_db.py # 五维监控（TOK→GEN→CPU→GPU→MEM）运行日志本地持久化存储
│   └── utils/ # 全局通用工具集
│       ├── __init__.py # 工具包初始化导出
│       ├── logger.py # 全局标准化日志管理，自动轮转清理
│       ├── monitor/ # 硬件资源采集工具三级目录
│       │   ├── hardware_collect.py # CPU/GPU/内存/主板SN硬件指标采集
│       │   ├── monitor_scheduler.py # 监控数据定时刷新调度器
│       │   └── log_writer.py # 本地日志7天自动清理工具
│       ├── process/ # 快照、TXT导入导出处理工具
│       └── i18n/ # 多语言本地配置加载工具
├── web/ # 纯原生HTML/CSS/JS前端，无TS/前端框架，PyWebView直接加载【前端二级目录锁定】
│   ├── index.html # 前端全局总入口页面，内置账号实时校验JS
│   ├── assets/ # 前端静态资源二级目录
│   │   ├── css/ # 全局样式三级目录
│   │   │   └── main.css # 统一页面全局样式表
│   │   ├── js/ # 原生JS工具三级目录
│   │   │   └── api_client.js # 前端本地HTTP/SSE请求SDK
│   │   └── i18n/ # 前端多语言JSON资源
│   │       ├── zh-CN.json
│   │       ├── en-US.json
│   │       ├── fr-FR.json
│   │       └── es-ES.json
│   ├── pages/ # 功能页面HTML三级目录
│   │   ├── login.html # 离线本地账号登录页面，前端实时正则校验
│   │   ├── workbench.html # 五级世界树创作工作台
│   │   ├── member.html # Lv9积分豁免/压测开关本地面板
│   │   ├── model_setting.html # 本地大模型参数配置页面
│   │   ├── monitor.html # 五维监控（TOK→GEN→CPU→GPU→MEM 标准顺序）面板
│   │   └── snapshot_export.html # 本地快照导入导出管理页
│   └── public/ # 前端公共工具二级目录
│       └── file_handler.js # 本地文件读写、上传下载原生脚本
├── tests/ # 单元测试、离线压测用例库【测试二级目录锁定】
│   ├── __init__.py # 测试包初始化
│   ├── account/ # 离线账号体系单元测试用例
│   └── core/ # AI生成、记忆引擎测试
│       └── pressure/ # 亿级字数离线压测专项用例
├── runtime/ # 程序运行时临时本地数据目录【运行缓存二级目录锁定】
│   ├── logs/ # 分级本地运行日志
│   │   ├── monitor_log/
│   │   │   └── monitor.log # 五维监控（TOK→GEN→CPU→GPU→MEM）运行日志
│   │   ├── runtime_log/
│   │   │   └── runtime.log # 程序运行主日志
│   │   └── token_flow_log/
│       └── token_flow.log # AI Token消耗日志
│   ├── cache/ # 冷热文本本地缓存目录
│   └── temp/ # 小节正文临时写入缓冲目录
├── data/ # 用户本地小说工程存储根目录【用户数据二级目录锁定】
│   ├── Book/ # 多小说工程隔离二级目录
│   │   ├── User/ # 本地用户全局配置三级目录
│   │   │   └── user_setting.json # 用户个性化离线配置
│   │   └──【自定义书名】/ # 单本小说独立工程目录
│   │       ├── db/ # 单本书本地元数据库
│   │       ├── chapters/ # 外置TXT章节正文（亿级字数分离存储）
│   │       ├── vector/ # 本地向量检索库
│   │       └── snapshot/ # 本地zip快照备份包
│   └── database/ # 全局统一SQLite账号数据库
├── assets/ # 项目全局静态资源（前后端共用）【静态资源二级目录锁定】
│   ├── lib/ # 全局多语言JSON资源
│   │   ├── zh-CN.json
│   │   ├── en-US.json
│   │   ├── fr-FR.json
│   │   └── es-ES.json
│   ├── fonts/ # 全局界面字体文件
│   └── images/ # Logo、界面图标静态图片
└── dist/ # CI自动打包全平台离线安装产物目录【打包产物二级目录锁定】
    ├── FeatherPen_V1.0.0_Windows_Setup.exe # Windows标准离线安装包
    ├── FeatherPen_V1.0.0_Windows_Portable.zip # Windows绿色便携离线包
    ├── FeatherPen_V1.0.0_macOS.dmg # macOS离线镜像包
    ├── FeatherPen_V1.0.0_Linux.AppImage # Linux单文件离线程序
    ├── FeatherPen_V1.0.0_amd64.deb # Debian系离线安装包
    ├── FeatherPen_V1.0.0_amd64.rpm # RHEL系离线安装包
    ├── FeatherPen_V1.0.0_Web_Docker.zip # 离线Web容器部署包
    ├── FeatherPen_V1.0.0_Android.apk # Android离线客户端
    ├── FeatherPen_V1.0.0_Chrome_Plugin.zip # Chrome离线浏览器插件
    └── FeatherPen_V1.0.0_VSCode_Plugin.zip # VSCode离线扩展

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

## 六、本次全量代码更新归档条目
FeatherPen/main.py | 删除废弃PyQt6双启动冗余代码，统一UTF8规范注释，修复路径拼接BUG
FeatherPen/init_env.py | 清理临时调试打印，标准化跨平台目录创建逻辑，统一文件读写编码
FeatherPen/config.yaml | 对齐开发文档账号、积分、模型全部国标参数规范
FeatherPen/member_config.json | 统一特权账号为6位UID，每条配置追加账号输入规范注释
FeatherPen/src/__init__.py | 新增账号查重离线接口，统一所有接口标准化返回格式
FeatherPen/src/account/local_login.py | 实现文档规定账号/密码前后端双层正则校验，兼容主板自动登录逻辑
FeatherPen/src/config/config_loader.py | 删除重复两套Config类冗余代码，重构标准单例模式，修复配置读取报错
FeatherPen/docs/STRUCTURE.md | 同步本次全量代码修改、新增文件，完整三级路径+标准化功能注释录入，融合完整目录树与国标架构规范
FeatherPen/docs/FeatherPen（羽笔）V1.0.0 开发文档.docx | 同步更新账号校验、数据库唯一索引、前后端双层校验全套规范章节