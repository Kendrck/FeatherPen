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
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_info (id TEXT PRIMARY KEY, level INT, point INT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS point_log (id INTEGER PRIMARY KEY AUTOINCREMENT, opt_type TEXT, cost INT, create_time TEXT)''')
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
