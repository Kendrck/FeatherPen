# FeatherPen/docs/STRUCTURE.md
# FeatherPen V1.0.0 世界树标准仓库完整目录架构文档
# 排序规则：文件夹优先按字母升序，同层级文件按英文字母升序排列
# 注释规范：# 后为文件/文件夹标准化业务说明，强制约束加粗标注
# 文档基准优先级：本目录规范 > 全平台兼容性规范 > 初代开发规范文档

FeatherPen/
├── .gitignore               # Git版本控制忽略规则
├── LICENSE                  # 开源许可证文件
├── pyproject.toml           # Python项目标准化构建配置
├── requirements.txt         # 生产环境依赖锁定清单
├── requirements-dev.txt     # 开发环境：单元测试/格式化/静态检查
├── init_env.py              # 跨平台环境一键初始化脚本
├── main.py                  # 项目**唯一全局启动入口**
├── .github/
│   └── workflows/           # CI/CD跨平台打包自动化脚本
├── docs/
│   ├── YESAPI_ACCOUNT.md    # YesApi云端测试账号对接文档
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── STRUCTURE.md
│   ├── DEVELOP.md
│   ├── API.md
│   ├── COMPATIBILITY.md
│   ├── PRESS_TEST.md        # 【新增】Lv9压测、亿级字数压力测试规范
│   ├── WORLD_TREE.md        # 【新增】五级世界树创作架构完整说明
│   └── TEMPLATE.md
├── src/
│   ├── __init__.py
│   ├── account/
│   │   ├── __init__.py
│   │   ├── account_login.py # 云端白名单校验、离线Lv0适配、权限下发
│   │   ├── member_ctrl.py   # 十级权限拦截、Lv9积分豁免/压测开关判定
│   │   └── point_system.py  # 积分扣费流水、100节自动校正扣费逻辑
│   ├── config/
│   │   ├── __init__.py
│   │   └── config_loader.py # 配置加载、非法参数回滚、URL自动清洗归一
│   ├── core/                # AI亿级长篇生成核心引擎【新增分层记忆/区间校正】
│   │   ├── __init__.py
│   │   ├── llm_api.py       # 三推理模式统一封装、Token统计、请求重试
│   │   ├── memory_filter.py # 三层冷热记忆、上下文优先级截断、防溢出核心
│   │   ├── role_extract.py  # 时序角色提取、分阶段人设存储
│   │   ├── novel_auto_gen.py# 五级大纲批量生成、全层级插叙、单章5节拦截校验
│   │   ├── world_check.py   # 100节定点区间校正、人设/时间线/伏笔全校验
│   │   └── progress_monitor.py # 30秒快照、断点续跑、进度持久化
│   ├── database/            # SQLite元数据持久化，正文外置TXT分离存储
│   │   ├── __init__.py
│   │   ├── db_sqlite.py     # 加密连接池、书籍元数据读写
│   │   └── monitor_db.py    # 监控/校正/Token日志持久化
│   └── utils/               # 通用工具、监控、多语言、快照恢复
│       ├── monitor/
│       ├── process/
│       └── i18n/
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── login_ui.py          # 登录页10个测试账号快捷按钮、离线隐藏逻辑
│   ├── novel_workbench.py   # 【新增】五级大纲可视化、单章5节拦截、插叙校正
│   ├── member_panel.py      # Lv9积分豁免+压测双开关、多语言状态提示
│   ├── model_setting_ui.py  # URL自动清洗、三模型切换界面
│   └── monitor_dashboard.py # 固定监控顺序TOK→GEN→CPU→GPU→MEM
├── tests/
│   ├── account/             # 账号/积分/开关测试用例
│   ├── core/                # 校正、记忆分层、批量生成单元测试
│   └── pressure/            # 【新增】亿级字数极限压测用例
├── runtime/
│   ├── logs/                # 监控/运行/Token日志，7天自动清理
│   ├── cache/               # 冷热记忆临时缓存
│   └── temp/                # 临时生成文件
├── data/                    # 【国标修改】原Book迁移至data，源码与用户数据彻底隔离
│   ├── Book/                # 单本小说独立工程目录
│   └── database/            # SQLite加密数据库存放目录
├── assets/
│   ├── lib/                 # 多语言包（登录/会员/工作台全部文案）
│   ├── fonts/
│   └── images/
└── dist/                    # 各平台打包产物

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