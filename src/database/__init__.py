#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库模块统一导出入口

提供 DatabaseManager、AccountRepository、PointsRepository 及初始化函数的快捷导入。
"""

from src.database.account_repo import AccountRepository
from src.database.db_sqlite import DatabaseManager, db, init_database
from src.database.points_repo import PointsRepository

__all__ = [
    "DatabaseManager",
    "db",
    "init_database",
    "AccountRepository",
    "PointsRepository",
]
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库模块统一导出入口

提供 DatabaseManager、AccountRepository、PointsRepository 及初始化函数的快捷导入。
"""

from src.database.account_repo import AccountRepository
from src.database.db_sqlite import DatabaseManager, db, init_database
from src.database.points_repo import PointsRepository

__all__ = [
    "DatabaseManager",
    "db",
    "init_database",
    "AccountRepository",
    "PointsRepository",
]
