# -*- coding: utf-8 -*-
"""
SQLite数据库核心封装模块 V1.0.0
功能：数据库初始化、数据表创建、连接池管理、标准化增删改查封装
适配AES加密、跨平台数据持久化
"""

import sqlite3

from src.config.config_loader import load_global_config


def init_database():
    """
    初始化数据库与核心数据表
    创建用户信息表、积分流水日志表
    """
    config = load_global_config()
    db_path = config["database"]["db_path"]
    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 核心数据表创建
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user_info (id TEXT PRIMARY KEY, level INT, point INT)"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS point_log (id INTEGER PRIMARY KEY AUTOINCREMENT, opt_type TEXT, cost INT, create_time TEXT)"""
    )
    conn.commit()
    conn.close()


def db_query(sql: str, params: tuple = ()):
    """
    数据库查询通用封装
    :param sql: 查询SQL语句
    :param params: SQL参数元组
    :return: 查询结果集
    """
    config = load_global_config()
    conn = sqlite3.connect(config["database"]["db_path"])
    cursor = conn.cursor()
    cursor.execute(sql, params)
    res = cursor.fetchall()
    conn.close()
    return res


def db_insert(sql: str, params: tuple = ()):
    """
    数据库插入通用封装
    :param sql: 插入SQL语句
    :param params: SQL参数元组
    """
    config = load_global_config()
    conn = sqlite3.connect(config["database"]["db_path"])
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    conn.close()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLite 数据库核心引擎

负责 SQLite 数据库的连接管理、表结构初始化及基础 CRUD 操作。
采用 WAL 模式以支持高并发读取，所有操作均提供类型安全接口。
"""

import sqlite3
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.config.config_loader import load_global_config
from src.utils.logger import get_logger

# 初始化模块日志
logger = get_logger(__name__)

# 数据库文件路径
DB_PATH = Path(__file__).parent.parent.parent / "data" / "database" / "featherpen.db"


class DatabaseManager:
    """数据库管理器单例"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """初始化数据库连接"""
        if self._initialized:
            return

        # 确保数据库目录存在
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        # 创建连接并开启 WAL 模式
        self._conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")

        # 初始化表结构
        self._init_tables()
        self._initialized = True
        logger.info(f"数据库初始化完成: {DB_PATH}")

    def _init_tables(self):
        """初始化核心数据表"""
        cursor = self._conn.cursor()

        # 账号表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                is_vip BOOLEAN DEFAULT FALSE,
                status TEXT DEFAULT 'active',
                last_login DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 积分流水表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS points_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                change_amount INTEGER NOT NULL,
                type TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )
        """)

        # 创建索引
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_accounts_username ON accounts(username)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_points_account_time ON points_log(account_id, created_at)"
        )

        self._conn.commit()
        logger.info("数据库表结构初始化完成")

    def execute(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行查询并返回结果列表"""
        cursor = self._conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def execute_write(self, sql: str, params: tuple = ()) -> int:
        """执行写入操作并返回受影响行数"""
        cursor = self._conn.cursor()
        cursor.execute(sql, params)
        self._conn.commit()
        return cursor.rowcount

    def close(self):
        """关闭数据库连接"""
        if self._conn:
            self._conn.close()
            logger.info("数据库连接已关闭")


# 全局数据库实例
db = DatabaseManager()


def init_database():
    """初始化数据库（供 main.py 调用）"""
    _ = db
    logger.info("数据库模块初始化成功")
