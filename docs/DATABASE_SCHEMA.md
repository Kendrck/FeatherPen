# FeatherPen/docs/DATABASE_SCHEMA.md
# GB/T 8567 SQLite数据库完整国标规范
## 1 基础信息
数据库引擎：SQLite3 WAL并发模式
文件路径：FeatherPen/data/database/featherpen.db
编码：UTF-8无BOM
自动初始化：src/database/sql_init.sql，程序启动自动执行

## 2 核心主表 local_user（账号表）
CREATE TABLE IF NOT EXISTS local_user (
    uid CHAR(64) PRIMARY KEY,
    level TINYINT DEFAULT 0,
    password VARCHAR(128) NOT NULL,
    point BIGINT DEFAULT 999999999,
    bind_email VARCHAR(64) NULL,
    bind_phone VARCHAR(20) NULL,
    desc_text VARCHAR(256) NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login_time DATETIME NULL,
    status TINYINT DEFAULT 1
);
唯一索引约束：
CREATE UNIQUE INDEX idx_user_email ON local_user(bind_email);
CREATE UNIQUE INDEX idx_user_phone ON local_user(bind_phone);

字段说明：
uid：账号，127001游客 / 6位特权 / 自定义账号
level：会员等级0~9
password：本地存储密码，前端传参后端校验
point：全局固定积分999999999
bind_email：绑定邮箱全局唯一
bind_phone：绑定手机号全局唯一
create_time：账号创建时间
last_login_time：上次登录时间
status：1正常 0禁用

## 3 配套业务表
1. sign_record：每日签到积分流水，关联uid
2. book_project：小说工程基础信息，存储工程名、创建时间、路径
3. monitor_log：AI/硬件监控持久日志，脱敏账号密钥

## 4 初始化内置数据
自动插入特权账号：000000~999999十级6位账号，统一密码passwd
Lv0游客无需预插入，登录时自动匹配127001规则

## 5 数据库操作强制规范
1. 所有读写统一通过db_sqlite.py封装函数get_db_conn/get_account_info
2. 禁止项目内直接写原生sqlite3连接代码
3. 程序启动自动检查表，缺失自动执行建表语句
4. 无云端同步、数据库远程连接逻辑，纯本地文件存储