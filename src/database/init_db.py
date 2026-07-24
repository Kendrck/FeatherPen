"""
GB/T 8567-2006 国标业务注释
文件路径：FeatherPen/src/database/init_db.py
功能：首次启动时执行 sql_init.sql 初始化数据库
"""
import os
import sqlite3


def init_database():
    """初始化 SQLite 数据库，执行建表与十级账号导入"""
    db_dir = "data/database"
    db_path = os.path.join(db_dir, "featherpen.db")
    sql_path = "src/database/sql_init.sql"

    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)

    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn.executescript(sql_script)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("数据库初始化完成：data/database/featherpen.db")
