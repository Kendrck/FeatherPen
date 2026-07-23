# FeatherPen/docs/STRUCTURE.md
# FeatherPen V1.0.0 STRUCTURE文件结构树标准仓库完整目录架构文档
# 排序规则：文件夹优先按字母升序，同层级文件按英文字母升序排列
# 注释规范：# 后为文件/文件夹标准化业务说明，强制约束加粗标注
# 文档基准优先级：本目录规范 > 全平台兼容性规范 > 初代开发规范文档
# 架构变更说明：永久移除ui/PyQt6、electron目录，统一采用web/原生HTML + PyWebView桌面壳架构

FeatherPen/ # 【一级根目录】
├── .gitignore               # 一级文件：Git版本忽略配置
├── LICENSE                  # 一级文件：开源协议文本
├── pyproject.toml           # 一级文件：Python标准化构建配置
├── requirements.txt         # 一级文件：生产环境依赖清单（新增pywebview依赖，移除electron/pyqt6）
├── requirements-dev.txt     # 一级文件：开发/测试依赖
├── init_env.py              # 一级文件：跨平台一键环境初始化脚本
├── main.py                  # 一级文件：全局唯一启动入口；同时启动FastAPI + 拉起PyWebView桌面窗口
├── .github/ # 【一级文件夹】CI/CD自动化打包
│   └── workflows/ # 【二级文件夹】CI工作流
│       └── ci_build.yml     # 【三级文件】自动打包脚本，产物输出dist目录
├── docs/ # 【一级文件夹】项目归档文档库
│   ├── README.md            # 【二级文件】项目快速上手（标注V1.0纯离线，在线功能V2.0）
│   ├── CHANGELOG.md         # 【二级文件】全版本迭代日志
│   ├── STRUCTURE.md         # 【二级文件】世界树目录追溯核心文档
│   ├── DEVELOP.md           # 【二级文件】本地开发部署指南
│   ├── API.md               # 【二级文件】后端接口规范（区分离线V1.0/在线V2.0预留接口）
│   ├── COMPATIBILITY.md     # 【二级文件】全平台适配+dist打包规范
│   ├── CONTRIBUTION.md      # 【二级文件】开发者协作规范
│   ├── TEMPLATE.md          # 【二级文件】配置模板说明
│   ├── YESAPI_ACCOUNT.md    # 【二级文件】云端对接预留文档（V2.0开发，V1.0不实现）
│   ├── WORLD_TREE.md        # 【二级文件】小说五级创作剧情架构专项文档
│   ├── PRESS_TEST.md        # 【二级文件】Lv9亿级压测操作规范
│   └── local_member_config_v1.0.0.json # 【二级文件】V1.0离线会员基准配置，存储10组6位特权账号，后端统一读取
├── src/ # 【一级文件夹】Python Core后端内核（FastAPI内置）
│   ├── __init__.py          # 【二级文件】源码包导出入口
│   ├── account/ # 【二级文件夹】离线账号模块（无云端交互，读取docs会员配置）
│   │   ├── __init__.py      # 【三级文件】模块初始化
│   │   ├── local_login.py   # 【三级文件】V1.0纯本地登录校验，匹配docs内6位UID账号，无主板SN云端校验
│   │   ├── member_ctrl.py   # 【三级文件】离线Lv0~Lv9权限本地判定，权限基准来自会员JSON
│   │   └── point_system.py  # 【三级文件】本地积分扣费逻辑，所有账号统一积分999999999
│   ├── config/ # 【二级文件夹】全局配置加载模块
│   │   ├── __init__.py      # 【三级文件】模块初始化
│   │   └── config_loader.py # 【三级文件】yaml/json加载，自动读取docs/local_member_config_v1.0.0.json、非法参数回滚
│   ├── core/ # 【二级文件夹】AI生成核心引擎
│   │   ├── __init__.py      # 【三级文件】模块初始化
│   │   ├── llm_api.py       # 【三级文件】三模型本地SSE统一封装
│   │   ├── memory_filter.py # 【三级文件】三层冷热记忆、Token截断
│   │   ├── role_extract.py  # 【三级文件】自动角色提取归档
│   │   ├── novel_auto_gen.py# 【三级文件】五级大纲、单章5节拦截逻辑
│   │   ├── world_check.py   # 【三级文件】100节区间剧情校验
│   │   └── progress_monitor.py # 【三级文件】30秒快照、断点持久化
│   ├── database/ # 【二级文件夹】SQLite本地持久层
│   │   ├── __init__.py      # 【三级文件】模块初始化
│   │   ├── db_sqlite.py     # 【三级文件】加密本地连接池、元数据CRUD
│   │   └── monitor_db.py    # 【三级文件】硬件日志本地持久化
│   └── utils/ # 【二级文件夹】通用工具集
│       ├── __init__.py      # 【三级文件】工具包初始化
│       ├── monitor/ # 【三级文件夹】硬件采集工具
│       │   ├── hardware_collect.py # 【三级文件】CPU/GPU/内存采集
│       │   ├── monitor_scheduler.py # 【三级文件】监控刷新调度
│       │   └── log_writer.py # 【三级文件】7天自动清理日志
│       ├── process/ # 【三级文件夹】快照、TXT导入导出工具
│       └── i18n/ # 【三级文件夹】多语言本地加载工具
├── web/ # 【一级文件夹】纯原生HTML/CSS/JS前端（PyWebView桌面窗口唯一加载源，废弃PyQt6/Electron）
│   ├── index.html           # 【二级文件】前端总入口页面
│   ├── assets/ # 【二级文件夹】前端静态资源
│   │   ├── css/ # 【三级文件夹】全局样式
│   │   │   └── main.css     # 【三级文件】全局样式表
│   │   ├── js/ # 【三级文件夹】原生JS工具（移除TS）
│   │   │   └── api_client.js # 【三级文件】前端原生HTTP/SSE请求工具
│   │   └── i18n/ # 【三级文件夹】多语言JSON包
│   │       ├── zh-CN.json
│   │       ├── en-US.json
│   │       ├── fr-FR.json
│   │       └── es-ES.json
│   ├── pages/ # 【二级文件夹】功能页面HTML
│   │   ├── login.html       # 【三级文件】本地离线登录页，读取docs会员配置渲染账号规则
│   │   ├── workbench.html   # 【三级文件】五级世界树工作台
│   │   ├── member.html      # 【三级文件】Lv9双开关本地面板
│   │   ├── model_setting.html # 【三级文件】模型配置页面
│   │   ├── monitor.html     # 【三级文件】五维监控面板
│   │   └── snapshot_export.html # 【三级文件】快照导入导出页面
│   └── public/ # 【二级文件夹】前端公共工具
│       └── file_handler.js  # 【三级文件】文件上传下载原生脚本
├── tests/ # 【一级文件夹】单元/压测用例
│   ├── __init__.py          # 【二级文件】测试包初始化
│   ├── account/ # 【二级文件夹】离线账号单元测试，基准为docs会员JSON
│   └── core/ # 【二级文件夹】生成/记忆测试
│       └── pressure/ # 【三级文件夹】亿级压测专项用例
├── runtime/ # 【一级文件夹】运行时临时本地数据
│   ├── logs/ # 【二级文件夹】分级本地日志
│   │   ├── monitor_log/
│   │   │   └── monitor.log
│   │   ├── runtime_log/
│   │   │   └── runtime.log
│   │   └── token_flow_log/
│   │       └── token_flow.log
│   ├── cache/ # 【二级文件夹】冷热本地缓存
│   └── temp/ # 【二级文件夹】小节临时写入缓冲
├── data/ # 【一级文件夹】纯本地用户小说工程（无网络上传）
│   ├── Book/ # 【二级文件夹】多小说隔离目录
│   │   ├── User/ # 【三级文件夹】本地用户配置
│   │   │   └── user_setting.json # 【三级文件】本地个性化配置
│   │   └──【自定义书名】/ # 【三级文件夹】单本独立本地工程
│   │       ├── db/ # 本地元数据库
│   │       ├── chapters/ # 外置TXT正文（亿级分离）
│   │       ├── vector/ # 本地向量库
│   │       └── snapshot/ # 本地zip快照包
│   └── database/ # 【二级文件夹】全局本地SQLite库
├── assets/ # 【一级文件夹】全局静态资源（前端web共用）
│   ├── lib/ # 【二级文件夹】全局多语言JSON
│   │   ├── zh-CN.json
│   │   ├── en-US.json
│   │   ├── fr-FR.json
│   │   └── es-ES.json
│   ├── fonts/ # 【二级文件夹】全局字体
│   └── images/ # 【二级文件夹】界面图标、Logo
└── dist/ # 【一级文件夹】CI自动打包全平台离线安装包
    ├── FeatherPen_羽笔_V1.0.0_Windows_Setup.exe       # Windows标准安装包
    ├── FeatherPen_羽笔_V1.0.0_Windows_Portable.zip    # Windows绿色便携压缩包
    ├── FeatherPen_羽笔_V1.0.0_macOS.dmg               # MacOS离线镜像包
    ├── FeatherPen_羽笔_V1.0.0_Linux.AppImage          # Linux单文件运行包
    ├── FeatherPen_羽笔_V1.0.0_Linux_amd64.deb         # Debian/Ubuntu安装包
    ├── FeatherPen_羽笔_V1.0.0_Linux_amd64.rpm         # CentOS/RHEL安装包
    ├── FeatherPen_羽笔_V1.0.0_Android.apk             # Android移动端APP安装包
    ├── FeatherPen_羽笔_V1.0.0_Web_Docker.zip          # Web离线Docker部署包
    ├── FeatherPen_羽笔_V1.0.0_Chrome_Plugin.zip        # Chrome离线插件包
    └── FeatherPen_羽笔_V1.0.0_VSCode_Plugin.zip       # VSCode离线扩展包
    
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
