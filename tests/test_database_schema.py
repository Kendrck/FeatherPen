import sqlite3
import unittest
from pathlib import Path

from src.database.init_db import init_database


class DatabaseSchemaTests(unittest.TestCase):
    def test_users_table_is_created(self) -> None:
        """验证数据库初始化脚本会创建 users 表。"""
        db_path = Path(__file__).resolve().parents[1] / "data" / "database" / "featherpen.db"
        if db_path.exists():
            db_path.unlink()

        init_database()

        conn = sqlite3.connect(db_path)
        try:
            row = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
            ).fetchone()
            self.assertIsNotNone(row)
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
