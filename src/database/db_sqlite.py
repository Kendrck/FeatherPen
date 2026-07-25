"""SQLite 数据库访问层。"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from src.config.config_loader import load_config


def get_db_conn() -> sqlite3.Connection:
    """获取本地数据库连接。"""
    cfg = load_config()
    root = Path(__file__).resolve().parents[1]
    db_dir = root / "data" / "database"
    db_path = db_dir / cfg["database"]["db_path"]

    db_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def db_get_user_info(uid: str) -> Optional[dict]:
    """根据 UID 查询本地账号完整信息。"""
    conn = get_db_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT uid, level, password, point FROM local_user WHERE uid = ?",
            (uid,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "uid": row[0],
            "level": row[1],
            "password": row[2],
            "point": row[3],
        }
    finally:
        conn.close()
