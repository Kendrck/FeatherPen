-- GB/T 8567 本地用户数据表初始化脚本
-- 约束：用户名/邮箱/手机号全局唯一，适配Lv0~Lv9十级离线账号
CREATE TABLE IF NOT EXISTS local_user (
    uid CHAR(64) NOT NULL PRIMARY KEY COMMENT '账号/用户名/邮箱，6-20位合规字符，特权6位数字兼容',
    level TINYINT NOT NULL DEFAULT 0 COMMENT '会员等级0~9，0=离线游客',
    password VARCHAR(128) NOT NULL COMMENT '登录密码，最少6位字符',
    point BIGINT NOT NULL DEFAULT 999999999 COMMENT '全局统一固定积分',
    bind_email VARCHAR(64) NULL COMMENT '绑定邮箱，全局唯一不可重复',
    bind_phone VARCHAR(20) NULL COMMENT '绑定手机号，全局唯一不可重复',
    desc_text VARCHAR(256) NULL COMMENT 账号等级备注说明',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '账号本地创建时间',
    last_login_time DATETIME NULL COMMENT '上次登录时间',
    status TINYINT NOT NULL DEFAULT 1 COMMENT 账号状态1正常/0禁用
);
-- 底层唯一索引，杜绝邮箱、手机号重复绑定
CREATE UNIQUE INDEX idx_user_email ON local_user(bind_email);
CREATE UNIQUE INDEX idx_user_phone ON local_user(bind_phone);
-- 积分流水记录表
CREATE TABLE IF NOT EXISTS point_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid CHAR(64) NOT NULL,
    opt_type VARCHAR(32) NOT NULL COMMENT 操作类型gen_chapter/sort_role等,
    cost INT NOT NULL COMMENT 变动积分数,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- 书籍工程记录表
CREATE TABLE IF NOT EXISTS book_project (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL UNIQUE,
    save_path TEXT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);