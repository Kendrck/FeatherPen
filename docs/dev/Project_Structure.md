```markdown
# FeatherPen V1.0.0 项目结构标准文档

**文档版本**：V1.0.0
**最后更新**：2026-07-21
**维护部门**：架构组


## 一、目录架构（强制规范）

项目目录严格分层解耦，业务源码、工具库、界面、数据、日志、测试模块完全独立。禁止新建散落文件、禁止跨目录乱序调用，所有文件存放路径严格遵循以下结构：

```
FeatherPen/
│
├── main.py                          # 全局唯一启动入口
│                                    # 负责环境初始化、服务加载及UI调度
│
├── pyproject.toml                   # 现代Python项目标准化配置
│                                    # 管理元数据、依赖及打包构建
│
├── config.yaml                      # 全局核心配置文件
│                                    # 统一定义系统、模型、监控及路径参数
│
├── .env.example                     # 环境变量模板
│                                    # 提供API密钥等敏感信息的配置占位符
│
├── requirements.txt                 # 项目依赖清单
│                                    # 锁定版本以确保跨平台环境一致性
│
├── init_env.py                      # 跨平台环境初始化脚本
│                                    # 自动创建虚拟环境并安装依赖
│
├── .gitignore                       # 版本控制忽略规则
│                                    # 排除缓存、日志、虚拟环境及用户隐私数据
│
├── src/                             # 核心源码目录
│   │                                存放所有业务逻辑与工具模块
│   ├── __init__.py                  # 源码包初始化
│   │                                统一导出核心模块与公共接口
│   │
│   ├── account/                     # 账号与会员体系模块
│   │   ├── __init__.py              # 模块初始化文件
│   │   ├── account_login.py         # 登录校验、账号状态检测及注销权限回退
│   │   ├── member_ctrl.py           # 会员等级动态适配、权限规则校验与拦截
│   │   └── point_system.py          # 积分扣费、统计、每日上限校验及流水记录
│   │
│   ├── config/                      # 全局配置管理模块
│   │   ├── __init__.py              # 模块初始化文件
│   │   └── config_loader.py         # 统一加载YAML配置与环境变量
│   │                                提供参数容错与自动回滚
│   │
│   ├── core/                        # AI创作核心引擎模块
│   │   ├── __init__.py              # 模块初始化文件
│   │   ├── llm_api.py               # 多模型接口统一适配、请求封装及异常重试
│   │   ├── memory_filter.py         # 上下文记忆智能筛选与历史投喂内容过滤
│   │   ├── role_extract.py          # 角色自动提取、特征归档及数据去重逻辑
│   │   ├── novel_auto_gen.py        # 全自动大纲规划、章节批量生成核心调度
│   │   ├── world_check.py           # 世界观、时间线及剧情逻辑一致性校验
│   │   └── progress_monitor.py      # AI生成进度、Token流量实时监控与调度
│   │
│   ├── database/                    # 数据持久化模块
│   │   ├── __init__.py              # 模块初始化文件
│   │   ├── db_sqlite.py             # SQLite数据库连接池、增删改查ORM封装
│   │   └── monitor_db.py            # 监控日志、生成进度及流量数据持久化存储
│   │
│   └── utils/                       # 通用工具库模块
│       │                            无业务耦合的纯工具能力
│       ├── __init__.py              # 模块初始化文件
│       ├── audio/                   # TTS语音合成与朗读工具封装
│       │   └── __init__.py
│       ├── monitor/                 # 系统监控采集与日志工具
│       │   ├── __init__.py
│       │   ├── hardware_collect.py  # CPU、内存、GPU等硬件指标采集
│       │   ├── monitor_scheduler.py # 监控任务刷新频率调度与双任务独立运行
│       │   └── log_writer.py        # 日志规范化写入、分级管理及7天自动清理
│       ├── process/                 # 进度快照、断点续跑及状态恢复工具
│       │   └── __init__.py
│       └── i18n/                    # 多语言国际化适配与翻译加载工具
│           └── __init__.py
│
├── ui/                              # PyQt6可视化界面模块
│   ├── main_window.py               # 主窗口初始化、页面路由及全局事件调度
│   ├── login_ui.py                  # 登录注册界面及账号状态可视化展示
│   ├── novel_workbench.py           # 小说创作工作台、生成操作面板及编辑器交互
│   ├── member_panel.py              # 会员等级、积分余额及专属权限展示面板
│   ├── model_setting_ui.py          # 模型参数微调、接口地址及密钥配置面板
│   └── monitor_dashboard.py         # 全维度硬件与Token流量监控仪表盘UI
│
├── tests/                           # 单元测试与集成测试目录
│   │                                保障核心业务逻辑稳定性
│   ├── __init__.py                  # 测试包初始化文件
│   ├── account/                     # 账号与会员模块测试用例
│   │   └── __init__.py
│   └── core/                        # AI核心引擎模块测试用例
│       └── __init__.py
│
├── docs/                            # 项目官方文档仓库
│   │                                存放开发规范与用户手册
│   ├── dev/                         # 开发规范文档目录
│   │   ├── Project_Structure.md     # 本文档 - 项目结构标准
│   │   ├── API_Spec.md              # API接口规范
│   │   ├── Code_Style.md            # 代码规范
│   │   ├── UI_Compatibility_Spec.md # 跨平台UI兼容规范
│   │   ├── Test_Guide.md            # 单元测试规范
│   │   └── Build_Guide.md           # 打包发布规范
│   └── user/                        # 用户文档目录
│       ├── Install_Guide.md         # 安装指南
│       ├── Language_Spec.md         # 多语言规范
│       ├── Data_Import_Export.md    # 数据导入导出规范
│       └── FAQ.md                   # 常见问题
│
├── logs/                            # 全局日志根目录
│   │                                运行期间自动创建
│   ├── monitor_log/                 # 硬件指标与监控任务运行日志
│   ├── runtime_log/                 # 程序运行状态、接口调用及异常报错日志
│   └── token_flow_log/              # Token上下行流量详细统计日志
│
└── Book/                            # 用户数据与书籍工程根目录
    │                                支持一键整体迁移与备份
    ├── User/                        # 全局用户公共配置目录
    │   └── user_setting.json        # 用户个性化配置文件
    │                                （主题、快捷键、默认模型等）
    │
    └── [自定义书名]/                # 独立小说工程隔离目录
        │                            确保多工程数据互不干扰
        ├── book_info.json           # 书籍基础元数据配置
        │                            （书名、作者、类型等）
        ├── role_list.json           # 全书角色归档数据
        │                            （姓名、性格、外貌特征等）
        ├── timeline.json            # 全书宏观时间线与重大事件节点数据
        ├── outline_full.json        # 全书完整卷章大纲数据
        ├── chapter_outline/         # 分章节细纲存储目录
        │   └── （按章节存储细纲文件）
        ├── chapter_content/         # 分章节正文内容存储目录
        │   └── （按章节存储正文文件）
        └── export/                  # 小说内容多格式导出文件存放目录
            └── （导出文件如 .docx .epub .txt 等）
```


## 二、模块依赖关系

依赖层级（自上而下）：

```
  UI层（ui/）
    │
    ├── 调用 ──→ src/account/      （会员、积分、登录）
    ├── 调用 ──→ src/core/         （生成、校验、监控）
    ├── 调用 ──→ src/database/     （数据持久化）
    └── 调用 ──→ src/utils/        （日志、监控采集）

  src/core/（核心引擎）
    │
    ├── 依赖 ──→ src/database/      （存储生成进度和监控数据）
    ├── 依赖 ──→ src/utils/         （日志、硬件监控）
    └── 依赖 ──→ src/config/        （读取配置参数）

  src/account/（账号体系）
    │
    ├── 依赖 ──→ src/database/      （存储用户积分流水）
    └── 依赖 ──→ src/config/        （读取会员配置）

  所有模块
    │
    └── 依赖 ──→ src/config/config_loader.py  （统一配置访问）
```


## 三、目录权限与约束

| 目录 | 约束规则 |
|------|----------|
| `src/` | 禁止在此目录下创建非模块目录 |
| `src/core/` | 禁止直接依赖UI层 |
| `src/utils/` | 禁止包含任何业务逻辑，仅提供纯工具函数 |
| `ui/` | 禁止直接操作数据库，必须通过 `src/` 下模块调用 |
| `Book/` | 用户数据目录，程序启动时自动检测，缺失则自动创建 |
| `logs/` | 程序运行期间自动创建，禁止手动修改日志文件 |
| `docs/` | 所有文档必须使用UTF-8编码，禁止二进制文件 |
| `tests/` | 测试文件命名必须为 `test_*.py` |


## 四、文件命名规范

| 文件类型 | 命名规范 | 示例 |
|----------|----------|------|
| Python源文件 | 小写字母 + 下划线 | `novel_auto_gen.py` |
| UI文件 | 小写字母 + 下划线 | `main_window.py` |
| 配置文件 | 小写字母 + 点分隔 | `config.yaml` |
| 文档文件（Markdown） | 大驼峰 + 下划线 | `Project_Structure.md` |
| 测试文件 | `test_` + 模块名 | `test_novel_auto_gen.py` |
| 数据文件（JSON） | 小写字母 + 下划线 | `role_list.json` |


## 五、版本历史

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|----------|------|
| V1.0.0 | 2026-07-21 | 初始版本，完整目录结构定义 | 架构组 |


## 六、文档维护说明

本文档为 FeatherPen V1.0.0 项目结构唯一官方标准，所有目录创建、文件存放必须严格遵循本文档。任何目录结构变更需同步更新本文档并记录版本历史。

---
**END**
```
