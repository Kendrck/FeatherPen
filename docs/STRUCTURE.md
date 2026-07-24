# FeatherPen/docs/STRUCTURE.md
# FeatherPen V1.0.0 STRUCTURE文件结构树标准仓库完整目录架构文档
# 排序规则：文件夹优先按字母升序，同层级文件按英文字母升序排列
# 注释规范：# 后为文件/文件夹标准化业务说明，强制约束加粗标注
# 文档基准优先级：本目录规范 > 全平台兼容性规范 > 初代开发规范文档
# 架构变更说明：永久移除ui/PyQt6、electron目录，统一采用web/原生HTML + PyWebView桌面壳架构

FeatherPen/ # 项目根一级目录
├── .gitignore # Git版本忽略配置文件
├── LICENSE # 开源协议文本
├── pyproject.toml # Python标准化构建配置，移除Electron/PyQt6打包配置
├── requirements.txt # 生产环境依赖，新增pywebview，删除electron、PyQt6
├── requirements-dev.txt # 开发/单元测试依赖清单
├── init_env.py # 跨平台离线环境一键初始化脚本
├── main.py # 全局唯一程序启动入口：异步启动FastAPI+拉起PyWebView桌面窗口
├── .github/ # CI/CD自动化流水线根目录
│   └── workflows/ # CI工作流二级目录
│       └── ci_build.yml # 全平台离线打包脚本，产物输出至dist目录
├── docs/ # 国标归档文档库，所有文件变更同步STRUCTURE.md
│   ├── README.md # 项目快速上手文档，标注V1.0纯离线、在线功能V2.0预留
│   ├── CHANGELOG.md # 版本迭代日志，区分离线V1.0与云端V2.0规划
│   ├── STRUCTURE.md # 世界树目录追溯核心文档，全项目文件路径归档
│   ├── DEVELOP.md # 本地离线开发部署指南
│   ├── API.md # 后端离线接口全集，云端接口仅注释预留
│   ├── COMPATIBILITY.md # 全平台适配与dist打包命名规范
│   ├── CONTRIBUTION.md # 开发者协作国标规范
│   ├── TEMPLATE.md # config/member_config配置模板说明
│   ├── YESAPI_ACCOUNT.md # V2.0云端对接预留文档，V1.0不开发代码
│   ├── WORLD_TREE.md # 小说五级世界树创作架构专项文档
│   └── PRESS_TEST.md # Lv9离线亿级字数压测操作规范
├── src/ # Python Core后端内核，FastAPI内置服务
│   ├── __init__.py # 源码包导出入口
│   ├── account/ # 离线本地账号模块，无云端交互
│   │   ├── __init__.py # 账号模块初始化
│   │   ├── local_login.py # 纯本地离线登录逻辑，无主板SN云端校验
│   │   ├── member_ctrl.py # Lv0~Lv9本地权限判定，6位UID校验
│   │   └── point_system.py # 本地积分扣费逻辑，全局固定积分999999999
│   ├── config/ # 全局配置加载模块
│   │   ├── __init__.py # 配置模块初始化
│   │   └── config_loader.py # yaml/json配置加载、非法参数自动回滚默认值
│   ├── core/ # AI长篇生成核心引擎
│   │   ├── __init__.py # 核心引擎初始化
│   │   ├── llm_api.py # 本地三模型SSE流式统一封装，无外网推理依赖
│   │   ├── memory_filter.py # 三层冷热本地记忆、Token截断处理
│   │   ├── role_extract.py # 小说角色自动提取、本地持久归档
│   │   ├── novel_auto_gen.py # 五级大纲生成、单章5节本地拦截逻辑
│   │   ├── world_check.py # 100节区间剧情人设/时间线本地校验
│   │   └── progress_monitor.py # 30秒本地快照、断电断点持久化
│   ├── database/ # SQLite本地加密持久层
│   │   ├── __init__.py # 数据库模块初始化
│   │   ├── db_sqlite.py # 加密本地连接池、小说元数据CRUD
│   │   └── monitor_db.py # 五维监控（TOK→GEN→CPU→GPU→MEM）运行日志本地持久化存储
│   └── utils/ # 全局通用工具集
│       ├── __init__.py # 工具包初始化
│       ├── monitor/ # 硬件资源采集工具三级目录
│       │   ├── hardware_collect.py # CPU/GPU/内存硬件指标采集
│       │   ├── monitor_scheduler.py # 监控数据定时刷新调度器
│       │   └── log_writer.py # 本地日志7天自动清理工具
│       ├── process/ # 快照、TXT导入导出处理工具
│       └── i18n/ # 多语言本地配置加载工具
├── web/ # 纯原生HTML/CSS/JS前端，无TS/前端框架，PyWebView直接加载
│   ├── index.html # 前端全局总入口页面
│   ├── assets/ # 前端静态资源二级目录
│   │   ├── css/ # 全局样式三级目录
│   │   │   └── main.css # 统一页面全局样式表
│   │   ├── js/ # 原生JS工具三级目录
│   │   │   └── api_client.js # 前端本地HTTP/SSE请求SDK
│   │   └── i18n/ # 前端多语言JSON资源包
│   │       ├── zh-CN.json
│   │       ├── en-US.json
│   │       ├── fr-FR.json
│   │       └── es-ES.json
│   ├── pages/ # 功能页面HTML三级目录
│   │   ├── login.html # 离线本地账号登录页面
│   │   ├── workbench.html # 五级世界树创作工作台
│   │   ├── member.html # Lv9积分豁免/压测开关本地面板
│   │   ├── model_setting.html # 本地大模型参数配置页面
│   │   ├── monitor.html # 五维监控（TOK→GEN→CPU→GPU→MEM 标准顺序）面板
│   │   └── snapshot_export.html # 本地快照导入导出管理页
│   └── public/ # 前端公共工具二级目录
│       └── file_handler.js # 本地文件读写、上传下载原生脚本
├── tests/ # 单元测试、离线压测用例库
│   ├── __init__.py # 测试包初始化
│   ├── account/ # 离线账号体系单元测试用例
│   └── core/ # AI生成、记忆引擎测试
│       └── pressure/ # 亿级字数离线压测专项用例
├── runtime/ # 程序运行时临时本地数据目录
│   ├── logs/ # 分级本地运行日志
│   │   ├── monitor_log/
│   │   │   └── monitor.log # 五维监控（TOK→GEN→CPU→GPU→MEM）运行日志
│   │   ├── runtime_log/
│   │   │   └── runtime.log # 程序运行主日志
│   │   └── token_flow_log/
│   │       └── token_flow.log # AI Token消耗日志
│   ├── cache/ # 冷热文本本地缓存目录
│   └── temp/ # 小节正文临时写入缓冲目录
├── data/ # 用户本地小说工程存储根目录，无网络上传逻辑
│   ├── Book/ # 多小说工程隔离二级目录
│   │   ├── User/ # 本地用户全局配置三级目录
│   │   │   └── user_setting.json # 用户个性化离线配置
│   │   └──【自定义书名】/ # 单本小说独立工程目录
│   │       ├── db/ # 单本书本地元数据库
│   │       ├── chapters/ # 外置TXT章节正文（亿级字数分离存储）
│   │       ├── vector/ # 本地向量检索库
│   │       └── snapshot/ # 本地zip快照备份包
│   └── database/ # 全局统一SQLite账号数据库
├── assets/ # 项目全局静态资源（前后端共用）
│   ├── lib/ # 全局多语言JSON资源
│   │   ├── zh-CN.json
│   │   ├── en-US.json
│   │   ├── fr-FR.json
│   │   └── es-ES.json
│   ├── fonts/ # 全局界面字体文件
│   └── images/ # Logo、界面图标静态图片
└── dist/ # CI自动打包全平台离线安装产物目录
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

    
# FeatherPen 国标项目架构规范（GB/T 8567-2006）
## 一、架构总则
1. 项目一、二级目录永久锁定，禁止修改、新增、删除
2. 仅支持三级及以下目录合规业务拓展
3. 所有模块分层解耦，符合商用软件工程标准化规范

## 二、固定一级目录职责
- src：核心业务源码、AI引擎、数据逻辑（核心业务层）
- ui：桌面可视化交互界面（视图层）
- docs：国标归档文档（全项目可追溯依据）
- tests：单元测试用例（质量校验层）
- runtime：运行缓存、日志、临时文件（运行支撑层）
- data：项目书籍工程、持久化数据（数据存储层）
- assets：静态资源、多语言、字体图片（资源层）
- dist：打包发布产物（发布层）

## 三、世界树五级国标层级
优先级自上而下不可逆，上层锁定下层剧情规则：
1. 世界树总纲：全局最高设定、世界观、核心规则（永久锁定）
2. 卷大纲：单卷主线、冲突、支线边界、登场角色
3. 章大纲：单章叙事目标、伏笔、收尾逻辑、时间节点
4. 小节小刚：单节轻量化提纲、远期记忆载体
5. 小节正文：最终生成内容、积分扣费唯一计量单元

## 四、数据存储国标规范
1. SQLite数据库：仅存储元数据、大纲、人设、统计数据
2. TXT外置存储：所有小节正文独立文件存储
3. 严格隔离结构化数据与大文本数据，实现亿级字数稳定运行

## 五、三级拓展规范
所有业务拓展、功能迭代、模块新增，必须在二级目录下新建三级文件/目录，禁止篡改顶层架构。
