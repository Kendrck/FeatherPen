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

# FeatherPen V1.0.0 STRUCTURE.md 世界树三级目录归档文档
执行标准：GB/T 8567-2006《计算机软件文档编制规范》
规则：所有新增/修改/删除三级文件必须录入下方清单，无归档则交付无效；一级、二级目录固定不可修改，仅三级拓展

# File Path_世界树完整三级文件结构树
FeatherPen/ # 项目根一级目录
├── .gitignore # Git版本忽略配置文件，屏蔽缓存、日志、打包产物、临时文件
├── LICENSE # MIT开源协议文本
├── pyproject.toml # Python标准化构建配置，移除Electron/PyQt6打包配置
├── requirements.txt # 生产环境依赖，包含pywebview，删除electron、PyQt6相关依赖
├── requirements-dev.txt # 开发/单元测试依赖清单
├── init_env.py # 跨平台离线环境一键初始化脚本，自动创建data/Book/User/127001游客目录，初始化网络端口配置
├── main.py # 全局唯一程序启动入口：异步启动FastAPI+拉起PyWebView桌面窗口
├── .github/
│   └── workflows/
│       └── ci_build.yml # 全平台离线打包CI脚本
├── docs/
│   ├── README.md # 项目总览快速上手文档
│   ├── CHANGELOG.md # 版本迭代变更日志
│   ├── STRUCTURE.md # 项目三级架构归档总文档（本文件）
│   ├── DEVELOP.md # 开发环境搭建、编码规范指南
│   ├── API.md # 全量后端离线API接口规范文档（核心接口手册）
│   ├── COMPATIBILITY.md # Windows/macOS/Linux全平台兼容性规范
│   ├── CONFIG_AND_API_SPEC.md # 全局配置文件、网络通信参数标准
│   ├── DATABASE_SCHEMA.md # SQLite本地数据库表结构、索引规范
│   ├── DEPLOYMENT_GUIDE.md # 全平台打包、部署交付指南
│   ├── PROJECT_OVERVIEW.md # 项目定位、离线隐私承诺、技术栈总说明
│   ├── ACCOUNT_SPEC.md # 离线账号、会员Lv0~Lv9权限、输入校验完整规范
│   ├── YESAPI_ACCOUNT.md # 预留云端账号扩展规范（V1.0不实现）
│   ├── PRESS_TEST.md # 压测规范，Lv9特权账号专属压测解锁规则
│   ├── local_member_config_v1.0.0.json # 会员等级配置标准模板
│   ├── dev/
│   │   ├── Project_Structure.md # 开发侧目录解读
│   │   ├── UI_Compatibility_Spec.md # 前端WebUI跨平台兼容规范
│   │   ├── Code_Style.md # Python/JS/HTML国标编码注释规范
│   │   ├── Test_Guide.md # 单元测试编写、执行规范
│   │   ├── Build_Guide.md # 打包脚本build.bat/setup.bat使用说明
│   ├── user/
│   │   ├── Install_Guide.md # 用户安装启动教程
│   │   ├── Language_Spec.md # 前端i18n多语言规范
│   │   ├── Data_Import_Export.md # 小说工程快照导入导出规范
│   │   ├── FAQ.md # 用户常见问题、端口冲突、登录报错解决方案
│   └── assets/ # 文档配图、配置模板
├── src/
│   ├── __init__.py # 后端根包初始化
│   ├── account/
│   │   ├── __init__.py
│   │   ├── local_login.py # 后端账号密码国标正则双层校验核心逻辑
│   │   ├── member_ctrl.py # 会员等级权限控制、积分读取逻辑
│   │   └── point_system.py # 全局积分统一管理，固定积分999999999
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_loader.py # 配置加载器，优先级：内置默认 < config.yaml < 环境变量
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm_api.py # 本地大模型推理接口封装（127.0.0.1:1234/v1）
│   │   ├── memory_filter.py # 对话记忆过滤脱敏逻辑
│   │   ├── role_extract.py # 小说人物角色自动提取
│   │   ├── novel_auto_gen.py # 章节、大纲自动生成核心业务
│   │   ├── world_check.py # 世界设定一致性校验功能
│   │   └── progress_monitor.py # AI生成进度监控
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_sqlite.py # SQLite数据库连接、通用操作封装
│   │   ├── monitor_db.py # 运行日志数据库读写
│   │   └── sql_init.sql # SQLite初始化脚本，local_user表唯一索引创建
│   └── utils/
│       ├── __init__.py
│       ├── monitor/
│       │   ├── monitor_scheduler.py # 后台监控定时任务调度
│       │   └── log_writer.py # 日志自动脱敏，密钥账号不明文输出
│       ├── process/ # 子进程管理工具
│       └── i18n/ # 多语言翻译工具
├── web/
│   ├── index.html # 桌面窗口首页，内置前端账号密码实时校验JS
│   ├── assets/
│   │   ├── css/
│   │   │   └── main.css # 全局前端样式统一规范
│   │   ├── js/
│   │   │   └── api_client.js # 前端接口请求统一封装
│   │   └── i18n/ # 多语言文本资源
│   ├── pages/
│   │   ├── login.html # 独立登录页面，前端实时输入校验拦截非法账号密码
│   │   ├── workbench.html # 小说创作工作台主页面
│   │   ├── member.html # 会员等级、积分、特权开关面板
│   │   ├── model_setting.html # 本地LLM模型地址配置页
│   │   ├── monitor.html # 运行监控、token、生成进度面板
│   │   └── snapshot_export.html # 小说工程快照导出页面
│   └── public/
│       └── file_handler.js # 本地文件读写、快照导出工具JS
├── tests/
│   ├── __init__.py
│   ├── account/ # 账号校验单元测试用例
│   └── core/
│       └── pressure/ # Lv9压测功能单元测试
├── runtime/
│   ├── logs/
│   │   ├── monitor_log/
│   │   │   └── monitor.log # 后台监控日志
│   │   ├── runtime_log/
│   │   │   └── runtime.log # 程序主运行日志
│   │   └── token_flow_log/
│       └── token_flow.log # AI token消耗日志
│   ├── cache/ # 临时缓存文件目录
│   └── temp/ # 临时导出文件目录
├── data/
│   ├── Book/
│   │   ├── User/
│   │   │   └── 127001/ # Lv0离线游客固定数据目录，init_env自动生成
│   │   └──【自定义书名】/ # 用户独立小说工程目录
│   │       ├── db/ # 单本小说本地数据库
│   │       ├── chapters/ # 章节文本存储
│   │       ├── vector/ # 文本向量缓存
│   │       └── snapshot/ # 工程快照备份
│   └── database/ # 全局账号加密数据库featherpen.db存放目录
├── assets/
│   ├── lib/ # 本地第三方静态库
│   ├── fonts/ # 桌面端字体资源
│   └── images/ # UI图片、图标资源
├── dist/ # 全平台打包输出产物目录
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
├── config.yaml # 全局网络、离线安全固化配置
├── member_config.json # Lv0~Lv9会员等级、权限、积分全局配置
├── .env.example # 环境变量覆盖配置模板
├── build.bat # Windows一键打包脚本
├── setup.bat # Windows环境初始化脚本

## V1.0.0 标准化校正变更归档（永久留存）
FeatherPen/init_env.py | 离线环境初始化，自动创建data/Book/User/127001游客目录，初始化网络端口默认配置，删除硬件采集目录创建逻辑
FeatherPen/src/account/local_login.py | 后端账号密码国标双层正则校验，拦截非法接口绕过请求，兼容特权账号与离线游客，修正8位UID错误为6位数字特权账号
FeatherPen/src/database/sql_init.sql | local_user表结构升级，新增bind_email、bind_phone字段，创建全局唯一索引防重复绑定，删除硬件关联字段
FeatherPen/web/index.html | 首页登录框前端实时账号/密码校验，标准化输入占位与错误提示文案，移除硬件自动登录DOM
FeatherPen/web/pages/login.html | 独立登录页JS校验逻辑，输入失焦、登录点击触发格式拦截，清除Electron/PyQt6兼容代码
FeatherPen/src/config/config_loader.py | 网络端口、离线UID配置优先级加载，支持环境变量FP_NETWORK_PREFERRED_PORT、FP_SECURITY_OFFLINE_UID覆盖，固化127.0.0.1绑定地址
FeatherPen/member_config.json | 全等级账号配置统一修正UID为6位数字，密码标准化为passwd，统一标注账号校验规范，固化Lv0~Lv9积分999999999
FeatherPen/config.yaml | 固化TCP网络全套参数、离线游客固定UID配置项，删除0.0.0.0绑定配置分支
FeatherPen/docs/ACCOUNT_SPEC.md | 补全离线账号三层校验机制、豁免账号规则、输入正则标准，修正GitHub 8位UID错误
FeatherPen/docs/API.md | 补全全部后端离线API请求/响应、权限、错误码完整规范
FeatherPen/docs/CONFIG_AND_API_SPEC.md | 补全网络通信超时、并发、线程池全套固化参数说明
FeatherPen/docs/DATABASE_SCHEMA.md | 完整梳理local_user表字段、唯一索引、约束国标规范
FeatherPen/docs/STRUCTURE.md | 重构完整世界树三级目录，删除废弃ui/electron目录归档记录
FeatherPen/docs/dev/Build_Guide.md | 更新打包命名模板，废弃Electron/PyQt6打包流程说明
FeatherPen/docs/user/FAQ.md | 补充端口冲突、账号格式报错、杀毒误报解决方案（硬件采集模块已删除）
FeatherPen/.gitignore | 新增dist、runtime/logs、runtime/cache、runtime/temp屏蔽规则，删除旧ui/electron缓存忽略项
FeatherPen/main.py | 清理PyQt6/Electron启动分支，仅保留FastAPI+PyWebView标准化启动流程
FeatherPen/pyproject.toml | 删除PyQt6、electron打包依赖配置，仅保留pywebview、FastAPI离线构建配置
FeatherPen/requirements.txt | 移除PyQt6、electron相关依赖包
FeatherPen/all_code.txt | 废弃临时文件，从目录树、仓库、构建脚本全量删除
FeatherPen/temp_dedup.py | 废弃临时文件，全项目删除
FeatherPen/app.ini | 非国标临时配置，全项目删除

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
