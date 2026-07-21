# Config配置模块统一导出规范
# 适配 docs/dev/Project_Structure.md 配置分层标准

from .db_sqlite import DB_CORE

# 配置模块公开接口白名单
__all__ = [
    "DB_CORE"
]
