# FeatherPen (羽笔) - 项目总览

## 1. 项目定位
FeatherPen 是一款基于 Python 的智能化内容生成与账号管理工具。项目采用模块化分层架构，旨在提供高可维护性、高扩展性的自动化业务处理能力。

## 2. 核心技术栈
- **语言**: Python 3.10+
- **配置管理**: YAML (config.yaml) + JSON (member_config.json)
- **依赖管理**: Poetry (pyproject.toml)
- **代码规范**: Ruff + Black
- **数据库**: SQLite (本地持久化) / Redis (缓存层，预留)

## 3. 目录结构规范
- `src/`: 核心业务逻辑层（API封装、AI生成、数据处理）。
- `ui/`: 用户交互层（CLI/GUI）。
- `data/`: 运行时数据（数据库文件、日志、临时缓存）。
- `docs/`: 标准化开发文档（接口定义、架构说明、部署指南）。
- `tests/`: 单元测试与集成测试脚本。
- `runtime/`: 运行时环境隔离区（虚拟环境、第三方二进制文件）。

## 4. 版本策略
当前主版本：V1.0.0
- 遵循语义化版本控制 (SemVer)。
- 所有重大架构变更需在 `docs/CHANGELOG.md` 中记录。