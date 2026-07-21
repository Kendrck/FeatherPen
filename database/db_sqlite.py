# -*- coding: utf-8 -*-
"""
FeatherPen羽笔 本地SQLite加密数据库操作类
文件路径：database/db_sqlite.py
功能：账号、积分、签到、书籍工程数据增删改查，AES加密敏感账号密码
依赖：config/config_loader.py 全局配置读取AES密钥、数据库路径
"""
import os
import sqlite3
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from config.config_loader import global_cfg, ROOT_PATH

# ====================== 全局常量读取 ======================
# 读取数据库文件路径
DB_FILE = ROOT_PATH / global_cfg.get_ini("database", "db_path")
# 读取16位AES加密密钥
AES_KEY = global_cfg.get_ini("crypto", "aes_key").encode("utf-8")

class SqliteDataBase:
    def __init__(self):
        """初始化数据库连接，自动创建数据表"""
        self.conn = None
        self.cursor = None
        # 初始化数据库连接
        self.connect_db()
        # 自动创建全部业务数据表
        self.create_all_table()

    def connect_db(self):
        """建立SQLite数据库连接，开启本地线程兼容"""
        self.conn = sqlite3.connect(str(DB_FILE), check_same_thread=False)
        self.cursor = self.conn.cursor()

    def aes_encrypt(self, raw_text: str) -> str:
        """
        AES加密明文（账号密码等敏感数据）
        :param raw_text: 原始明文字符串
        :return: 加密后base64字符串
        """
        iv = get_random_bytes(16)
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        raw_bytes = raw_text.encode("utf-8")
        encrypt_bytes = cipher.encrypt(pad(raw_bytes, AES.block_size))
        # 拼接iv+加密字节，转字符串存储
        return (iv + encrypt_bytes).hex()

    def aes_decrypt(self, encrypt_hex: str) -> str:
        """
        AES解密存储的加密字符串
        :param encrypt_hex: 数据库中存储的加密hex字符串
        :return: 原始明文
        """
        raw_data = bytes.fromhex(encrypt_hex)
        iv = raw_data[:16]
        encrypt_data = raw_data[16:]
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
        decrypt_bytes = unpad(cipher.decrypt(encrypt_data), AES.block_size)
        return decrypt_bytes.decode("utf-8")

    def create_all_table(self):
        """创建全部数据表：账号表、签到记录表、书籍工程表"""
        # 1. 账号表：存储账号、加密密码、会员等级、当前积分
        sql_account = """
        CREATE TABLE IF NOT EXISTS account(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT NOT NULL UNIQUE,
            encrypt_pwd TEXT NOT NULL,
            member_level INTEGER DEFAULT 0,
            current_point INTEGER DEFAULT 0
        )
        """
        self.cursor.execute(sql_account)

        # 2. 每日签到记录表：记录账号、签到日期，防止重复签到
        sql_sign = """
        CREATE TABLE IF NOT EXISTS sign_record(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT NOT NULL,
            sign_date TEXT NOT NULL,
            add_point INTEGER NOT NULL
        )
        """
        self.cursor.execute(sql_sign)

        # 3. 书籍工程记录表：记录本地创建的小说工程名、存储路径、创建时间
        sql_book = """
        CREATE TABLE IF NOT EXISTS book_project(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT NOT NULL UNIQUE,
            save_path TEXT NOT NULL,
            create_time TEXT NOT NULL
        )
        """
        self.cursor.execute(sql_book)
        self.conn.commit()

    # ========== 账号相关CRUD方法 ==========
    def register_account(self, account: str, pwd: str):
        """注册账号，密码加密存入数据库"""
        encrypt_pwd = self.aes_encrypt(pwd)
        sql = "INSERT INTO account(account, encrypt_pwd, member_level, current_point) VALUES (?,?,0,0)"
        self.cursor.execute(sql, (account, encrypt_pwd))
        self.conn.commit()

    def get_account_info(self, account: str):
        """根据账号查询会员等级、积分、加密密码"""
        sql = "SELECT encrypt_pwd, member_level, current_point FROM account WHERE account=?"
        res = self.cursor.execute(sql, (account,)).fetchone()
        if not res:
            return None
        encrypt_pwd, level, point = res
        # 解密密码返回完整信息
        real_pwd = self.aes_decrypt(encrypt_pwd)
        return {
            "account": account,
            "password": real_pwd,
            "member_level": level,
            "point": point
        }

    def update_point(self, account: str, point_change: int):
        """增减账号积分：point_change正数加积分，负数扣积分"""
        sql = "UPDATE account SET current_point = current_point + ? WHERE account=?"
        self.cursor.execute(sql, (point_change, account))
        self.conn.commit()

    def set_member_level(self, account: str, level: int):
        """修改账号会员等级（超级账号固定Lv9）"""
        sql = "UPDATE account SET member_level=? WHERE account=?"
        self.cursor.execute(sql, (level, account))
        self.conn.commit()

    # ========== 签到记录方法 ==========
    def check_sign_today(self, account: str, today_str: str) -> bool:
        """判断账号今日是否已签到，返回True=已签到"""
        sql = "SELECT id FROM sign_record WHERE account=? AND sign_date=?"
        res = self.cursor.execute(sql, (account, today_str)).fetchone()
        return res is not None

    def add_sign_record(self, account: str, today_str: str, add_point: int):
        """新增签到记录，发放签到积分"""
        sql = "INSERT INTO sign_record(account, sign_date, add_point) VALUES (?,?,?)"
        self.cursor.execute(sql, (account, today_str, add_point))
        self.conn.commit()
        # 同步增加账号积分
        self.update_point(account, add_point)

    # ========== 书籍工程记录方法 ==========
    def add_book_project(self, book_name: str, save_path: str, create_time: str):
        """新建小说工程写入数据库记录"""
        sql = "INSERT INTO book_project(book_name, save_path, create_time) VALUES (?,?,?)"
        self.cursor.execute(sql, (book_name, save_path, create_time))
        self.conn.commit()

    def close(self):
        """关闭数据库连接，程序退出调用"""
        if self.conn:
            self.conn.close()

# 全局数据库单例，全项目统一调用
db = SqliteDataBase()
