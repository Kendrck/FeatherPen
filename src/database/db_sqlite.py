"""
GB/T 8567-2006 国标业务注释
文件路径：FeatherPen/src/database/db_sqlite.py
功能：SQLite本地账号查询CRUD，配套登录校验
"""
import sqlite3

from src.config.config_loader import load_config


def get_db_conn():
    """获取加密本地数据库连接"""
    cfg = load_config()
    db_path = f"data/database/{cfg['database']['db_path']}"
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA key = ?", (cfg["crypto"]["aes_key"],))
    return conn

def db_get_user_info(uid: str) -> dict | None:
    """根据6位UID查询本地账号完整信息"""
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT uid, level, password, point FROM local_user WHERE uid = ?", (uid,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "uid": row[0],
        "level": row[1],
        "password": row[2],
        "point": row[3]
    }
"""
GB/T 8567-2006 国标业务注释
文件路径：FeatherPen/src/database/db_sqlite.py
功能：SQLite 本地账号查询 CRUD
约束：V1.0 先使用普通 SQLite，保证登录可运行
"""
import os


def get_db_conn():
    """获取本地数据库连接"""
    cfg = load_config()
    db_dir = "data/database"
    db_path = os.path.join(db_dir, cfg["database"]["db_path"])

    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn


def db_get_user_info(uid: str) -> dict | None:
    """根据6位UID查询本地账号完整信息"""
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT uid, level, password, point FROM local_user WHERE uid = ?",
        (uid,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "uid": row[0],
        "level": row[1],
        "password": row[2],
        "point": row[3]
    }
