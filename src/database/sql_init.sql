/*
GB/T 8567-2006 国标数据库注释
文件路径：FeatherPen/src/database/sql_init.sql
功能：SQLite全自动建表、业务索引、十级离线账号初始化
对齐member_config.json账号参数，纯本地无云端字段
监控表严格遵循TOK→GEN→CPU→GPU→MEM五维标准
*/
-- 1. 本地离线用户账号主表
CREATE TABLE IF NOT EXISTS local_user (
    uid CHAR(6) NOT NULL PRIMARY KEY COMMENT '6位数字唯一离线账号主键',
    level TINYINT NOT NULL DEFAULT 0 COMMENT '会员等级 0~9十级体系',
    password VARCHAR(128) NOT NULL COMMENT '本地加密存储登录密码',
    point BIGINT NOT NULL DEFAULT 999999999 COMMENT '全局统一固定积分',
    desc_text VARCHAR(256) NULL COMMENT '账号等级备注',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '账号创建时间',
    last_login_time DATETIME NULL COMMENT '最后本地登录时间',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '账号状态 0禁用/1正常'
) COMMENT '纯本地账号表，无云端同步逻辑';

-- 2. 小说工程隔离表
CREATE TABLE IF NOT EXISTS novel_project (
    project_id VARCHAR(32) NOT NULL PRIMARY KEY COMMENT '单本小说唯一ID',
    uid CHAR(6) NOT NULL COMMENT '归属用户6位UID',
    book_name VARCHAR(128) NOT NULL COMMENT '自定义书名',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    snapshot_count INT NOT NULL DEFAULT 0 COMMENT '本地快照数量',
    status TINYINT NOT NULL DEFAULT 1,
    FOREIGN KEY (uid) REFERENCES local_user(uid)
);

-- 3. 五级世界章节小节表
CREATE TABLE IF NOT EXISTS chapter_section (
    section_id VARCHAR(32) PRIMARY KEY,
    project_id VARCHAR(32) NOT NULL,
    chapter_id VARCHAR(32) NOT NULL,
    volume_id VARCHAR(32) NOT NULL,
    section_content TEXT NULL COMMENT '小节正文',
    section_sort INT NOT NULL DEFAULT 0,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_check TINYINT NOT NULL DEFAULT 0 COMMENT '1=完成100节剧情校正',
    FOREIGN KEY (project_id) REFERENCES novel_project(project_id)
);

-- 4. 五维监控日志表（标准顺序TOK→GEN→CPU→GPU→MEM）
CREATE TABLE IF NOT EXISTS monitor_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_flow FLOAT NOT NULL DEFAULT 0 COMMENT 'TOK令牌消耗',
    gen_progress FLOAT NOT NULL DEFAULT 0 COMMENT 'GEN生成进度',
    cpu_usage FLOAT NOT NULL DEFAULT 0 COMMENT 'CPU占用率',
    gpu_usage FLOAT NOT NULL DEFAULT 0 COMMENT 'GPU占用率',
    mem_usage FLOAT NOT NULL DEFAULT 0 COMMENT '内存占用率',
    record_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 业务查询索引
CREATE INDEX IF NOT EXISTS idx_user_level ON local_user(level);
CREATE INDEX IF NOT EXISTS idx_project_uid ON novel_project(uid);
CREATE INDEX IF NOT EXISTS idx_section_project ON chapter_section(project_id);
CREATE INDEX IF NOT EXISTS idx_monitor_time ON monitor_record(record_time);

-- 完整十级账号初始化（完全匹配配置文件）
INSERT OR IGNORE INTO local_user (uid, level, password, point, desc_text) VALUES
('111111', 1, 'passwd', 999999999, 'Lv1 初闻 本地离线测试账号'),
('222222', 2, 'passwd', 999999999, 'Lv2 薄名 本地离线测试账号'),
('333333', 3, 'passwd', 999999999, 'Lv3 浅露 本地离线测试账号'),
('444444', 4, 'passwd', 999999999, 'Lv4 知名 本地离线测试账号'),
('555555', 5, 'passwd', 999999999, 'Lv5 显赫 本地离线测试账号'),
('666666', 6, 'passwd', 999999999, 'Lv6 盛传 本地离线测试账号'),
('777777', 7, 'passwd', 999999999, 'Lv7 昭著 本地离线测试账号'),
('888888', 8, 'passwd', 999999999, 'Lv8 传奇 本地离线测试账号'),
('999999', 9, 'passwd', 999999999, 'Lv9 不朽 本地离线特权账号1'),
('000000', 9, 'passwd', 999999999, 'Lv9 不朽 本地离线特权账号2');