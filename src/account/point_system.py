"""
FeatherPen V1.0.0 积分扣费、统计与流水记录模块
功能：管理积分扣费、每日上限校验、积分流水记录
规范：统一扣费标准，Lv0离线账号积分只扣不加
"""
import json
import logging
import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, List
import time

# FeatherPen/src/account/point_system.py

import time

class PointSystem:
    """
    积分与会员时长计算系统
    """
    
    @staticmethod
    def calculate_expire_time(hours: int) -> int:
        """
        根据购买的时长计算会员过期时间戳
        :param hours: 购买的小时数
        :return: 过期时间的 Unix 时间戳
        """
        current_timestamp = int(time.time())
        return current_timestamp + (hours * 3600)

    @staticmethod
    def is_vip_active(expire_time: int) -> bool:
        """
        判断当前会员是否仍在有效期内
        """
        if expire_time == 0:
            return False
        return int(time.time()) < expire_time

logger = logging.getLogger(__name__)

class PointSystem:
    """
    积分管理系统，处理所有积分相关的操作
    """
    def __init__(self, db_path: str = "featherpen.db"):
        """
        初始化积分系统
        :param db_path: 数据库文件路径
        """
        self.db_path = Path(db_path)
        self._init_database()

    def _init_database(self) -> None:
        """初始化积分相关的数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS point_account (
                uid TEXT PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS point_flow (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT,
                amount INTEGER,
                flow_type TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_consumption (
                uid TEXT,
                consume_date TEXT,
                total_consumed INTEGER DEFAULT 0,
                PRIMARY KEY (uid, consume_date)
            )
        ''')
        conn.commit()
        conn.close()

    def get_balance(self, uid: str) -> int:
        """
        查询用户积分余额
        :param uid: 用户ID
        :return: 当前积分余额
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM point_account WHERE uid = ?', (uid,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def add_points(self, uid: str, amount: int, description: str = "") -> bool:
        """
        增加用户积分（仅用于登录奖励等场景）
        :param uid: 用户ID
        :param amount: 增加积分数量
        :param description: 操作描述
        :return: 操作成功返回True
        """
        if amount <= 0:
            return False
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO point_account (uid, balance) VALUES (?, ?) '
            'ON CONFLICT(uid) DO UPDATE SET balance = balance + ?',
            (uid, amount, amount)
        )
        cursor.execute(
            'INSERT INTO point_flow (uid, amount, flow_type, description) VALUES (?, ?, ?, ?)',
            (uid, amount, 'add', description)
        )
        conn.commit()
        conn.close()
        logger.info(f"用户 {uid} 增加积分 {amount}: {description}")
        return True

    def consume_points(self, uid: str, amount: int, description: str = "") -> bool:
        """
        扣除用户积分
        :param uid: 用户ID
        :param amount: 扣除积分数量
        :param description: 操作描述
        :return: 扣费成功返回True，余额不足返回False
        """
        if amount <= 0:
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 1. 检查余额是否充足
        cursor.execute('SELECT balance FROM point_account WHERE uid = ?', (uid,))
        result = cursor.fetchone()
        current_balance = result[0] if result else 0
        if current_balance < amount:
            conn.close()
            logger.warning(f"用户 {uid} 积分不足，需要 {amount}，当前 {current_balance}")
            return False

        # 2. 扣除积分
        cursor.execute(
            'UPDATE point_account SET balance = balance - ? WHERE uid = ?',
            (amount, uid)
        )
        cursor.execute(
            'INSERT INTO point_flow (uid, amount, flow_type, description) VALUES (?, ?, ?, ?)',
            (uid, -amount, 'consume', description)
        )

        # 3. 记录日消耗
        today = date.today().isoformat()
        cursor.execute(
            'INSERT INTO daily_consumption (uid, consume_date, total_consumed) '
            'VALUES (?, ?, ?) '
            'ON CONFLICT(uid, consume_date) DO UPDATE SET total_consumed = total_consumed + ?',
            (uid, today, amount, amount)
        )

        conn.commit()
        conn.close()
        logger.info(f"用户 {uid} 扣除积分 {amount}: {description}")
        return True

    def get_daily_consumed(self, uid: str) -> int:
        """
        获取用户当日已消耗积分
        :param uid: 用户ID
        :return: 当日已消耗积分总数
        """
        today = date.today().isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT total_consumed FROM daily_consumption WHERE uid = ? AND consume_date = ?',
            (uid, today)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def get_flow_history(self, uid: str, limit: int = 100) -> List[Dict]:
        """
        获取用户的积分流水历史
        :param uid: 用户ID
        :param limit: 返回记录条数限制
        :return: 流水记录列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT amount, flow_type, description, created_at FROM point_flow '
            'WHERE uid = ? ORDER BY created_at DESC LIMIT ?',
            (uid, limit)
        )
        results = cursor.fetchall()
        conn.close()
        return [
            {'amount': r[0], 'type': r[1], 'description': r[2], 'time': r[3]}
            for r in results
        ]

    def check_daily_limit(self, uid: str, daily_limit: int) -> bool:
        """
        检查用户当日消耗是否已达到上限
        :param uid: 用户ID
        :param daily_limit: 日消耗上限，-1表示无限制
        :return: 未达上限返回True，已达上限返回False
        """
        if daily_limit == -1:
            return True
        consumed = self.get_daily_consumed(uid)
        return consumed < daily_limit
