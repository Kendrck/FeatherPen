"""
GB/T 8567-2006 国标业务注释
文件路径：FeatherPen/src/database/init_db.py
功能：首次启动时执行 sql_init.sql 初始化数据库
"""
import sqlite3
from pathlib import Path


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    ).fetchone()
    return row is not None


def _add_column_if_missing(conn: sqlite3.Connection, table_name: str, column_def: str) -> None:
    if not _table_exists(conn, table_name):
        return
    columns = {row[1] for row in conn.execute(f"PRAGMA table_info({table_name})")}
    column_name = column_def.split()[0]
    if column_name not in columns:
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_def}")


def init_database():
    """初始化 SQLite 数据库，执行建表与十级账号导入"""
    project_root = Path(__file__).resolve().parents[2]
    db_dir = project_root / "data" / "database"
    db_path = db_dir / "featherpen.db"
    sql_path = project_root / "src" / "database" / "sql_init.sql"

    db_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    # ==========【关键修复】先执行建表SQL，再追加兼容字段 ==========
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()

    # 建表完成后，再执行旧数据库兼容新增字段
    _add_column_if_missing(conn, "local_user", "nickname VARCHAR(64) DEFAULT NULL")
    _add_column_if_missing(conn, "local_user", "password_hash VARCHAR(256) DEFAULT NULL")
    _add_column_if_missing(conn, "local_user", "is_admin TINYINT NOT NULL DEFAULT 0")
    _add_column_if_missing(conn, "local_user", "vip_level TINYINT NOT NULL DEFAULT 1")
    _add_column_if_missing(conn, "local_user", "vip_expire_at DATETIME DEFAULT NULL")
    _add_column_if_missing(conn, "local_user", "last_active_at DATETIME DEFAULT NULL")
    _add_column_if_missing(conn, "local_user", "is_deleted TINYINT NOT NULL DEFAULT 0")
    _add_column_if_missing(conn, "local_user", "deleted_at DATETIME DEFAULT NULL")
    _add_column_if_missing(conn, "users", "email TEXT DEFAULT NULL UNIQUE")
    _add_column_if_missing(conn, "users", "phone TEXT DEFAULT NULL UNIQUE")

    conn.commit()
    conn.close()
    print(f"✅ 数据库初始化完成 -> {db_path}")


if __name__ == "__main__":
    init_database()
