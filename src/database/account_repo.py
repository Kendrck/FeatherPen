#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
账号数据访问层 (Repository)

封装 accounts 表的 CRUD 操作，提供类型安全的数据库交互接口。
"""

from typing import Any, Dict, Optional

from src.database.db_sqlite import db
from src.utils.logger import get_logger

logger = get_logger(__name__)


class AccountRepository:
    """账号数据访问类"""

    @staticmethod
    def get_by_username(username: str) -> Optional[Dict[str, Any]]:
        """根据用户名查询账号"""
        sql = "SELECT * FROM accounts WHERE username = ? LIMIT 1"
        results = db.execute(sql, (username,))
        return results[0] if results else None

    @staticmethod
    def create(username: str, password_hash: str, level: int = 1) -> int:
        """创建新账号，返回自增ID"""
        sql = """
            INSERT INTO accounts (username, password_hash, level) 
            VALUES (?, ?, ?)
        """
        db.execute_write(sql, (username, password_hash, level))
        logger.info(f"新账号创建成功: {username}")
        # 获取最后插入的 ID
        result = db.execute("SELECT last_insert_rowid() as id")
        return result[0]["id"] if result else 0

    @staticmethod
    def update_last_login(username: str) -> None:
        """更新最后登录时间"""
        sql = "UPDATE accounts SET last_login = CURRENT_TIMESTAMP WHERE username = ?"
        db.execute_write(sql, (username,))

    @staticmethod
    def update_status(username: str, status: str) -> None:
        """更新账号状态"""
        sql = "UPDATE accounts SET status = ? WHERE username = ?"
        db.execute_write(sql, (status, username))
