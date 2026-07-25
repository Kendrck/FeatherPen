# -*- coding: utf-8 -*-
"""
GB/T 8567-2006 SQLite数据库访问层
文件路径: FeatherPen/src/database/db_sqlite.py
功能：数据库连接、自动执行初始化sql脚本、本地用户查询
约束：完全匹配sql_init.sql local_user数据表字段；自动创建目录+初始化表与测试账号
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

# 修复导入名称：load_config → load_global_config，与config_loader统一命名规范
from src.config.config_loader import load_global_config


def get_db_conn() -> sqlite3.Connection:
    """获取数据库连接，自动执行初始化脚本"""
    cfg = load_global_config()
    root = Path(__file__).resolve().parents[1]
    db_dir = root / "data" / "database"
    db_path = db_dir / cfg["database"]["db_path"]
    sql_script_path = root / "src" / "database" / "sql_init.sql"

    # 创建数据库目录
    db_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    # 设置行工厂，支持列名取值
    conn.row_factory = sqlite3.Row

    # 首次自动执行建表&账号初始化脚本
    if sql_script_path.exists():
        with open(sql_script_path, "r", encoding="utf-8") as f:
            sql_content = f.read()
        conn.executescript(sql_content)
        conn.commit()
    return conn

def get_account_info(uid: str) -> Optional[dict]:
    """
    根据UID查询local_user账号信息，字段完全对齐sql_init.sql
    :param uid: 用户账号字符串
    :return: 标准化字典 / None账号不存在
    """
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT uid, level, password, point FROM local_user WHERE uid = ?",
            (uid,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        # 转换为统一key字典，适配登录接口
        return {
            "account": row["uid"],
            "member_level": row["level"],
            "password": row["password"],
            "current_point": row["point"]
        }
    finally:
        conn.close()
