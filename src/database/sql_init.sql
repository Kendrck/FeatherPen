/*
GB/T 8567-2006 本地数据库初始化脚本 (SQLite适配版)
文件路径：FeatherPen/src/database/sql_init.sql
功能：SQLite全自动建表、业务索引、十级离线账号初始化
约束：用户名/邮箱/手机号全局唯一，无硬件关联字段，纯本地无云端字段
监控表严格遵循 TOK→GEN→CPU→GPU→MEM 五维标准
*/

-- 1. 本地离线用户账号主表
CREATE TABLE IF NOT EXISTS local_user (
    uid CHAR(64) NOT NULL PRIMARY KEY, -- 账号，特权6位数字/游客127001豁免校验
    level TINYINT NOT NULL DEFAULT 0, -- 会员等级 Lv0~Lv9
    password VARCHAR(128) NOT NULL, -- 本地加密存储密码，最低6位
    point BIGINT NOT NULL DEFAULT 999999999, -- 全账号统一固定积分
    bind_email VARCHAR(64) NULL, -- 绑定邮箱，全局唯一
    bind_phone VARCHAR(20) NULL, -- 绑定手机号，全局唯一
    desc_text VARCHAR(256) NULL, -- 账号备注
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 账号创建时间
    last_login_time DATETIME NULL, -- 最后登录时间
    status TINYINT NOT NULL DEFAULT 1 -- 账号状态 1正常 0禁用
);

-- 唯一索引，防止邮箱/手机号重复绑定账号
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_email ON local_user(bind_email);
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_phone ON local_user(bind_phone);

-- 2. 小说工程隔离表
CREATE TABLE IF NOT EXISTS novel_project (
    project_id VARCHAR(32) NOT NULL PRIMARY KEY, -- 单本小说唯一ID
    uid CHAR(64) NOT NULL REFERENCES local_user(uid), -- 归属用户UID(外键)
    book_name VARCHAR(128) NOT NULL, -- 自定义书名
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    snapshot_count INT NOT NULL DEFAULT 0, -- 本地快照数量
    status TINYINT NOT NULL DEFAULT 1
);

-- 3. 五级世界章节小节表
CREATE TABLE IF NOT EXISTS chapter_section (
    section_id VARCHAR(32) PRIMARY KEY,
    project_id VARCHAR(32) NOT NULL REFERENCES novel_project(project_id), -- 外键关联
    chapter_id VARCHAR(32) NOT NULL,
    volume_id VARCHAR(32) NOT NULL,
    section_content TEXT NULL, -- 小节正文
    section_sort INT NOT NULL DEFAULT 0,
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_check TINYINT NOT NULL DEFAULT 0 -- 1=完成100节剧情校正
);

-- 4. 五维监控日志表（标准顺序 TOK→GEN→CPU→GPU→MEM）
CREATE TABLE IF NOT EXISTS monitor_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_flow FLOAT NOT NULL DEFAULT 0, -- TOK令牌消耗
    gen_progress FLOAT NOT NULL DEFAULT 0, -- GEN生成进度
    cpu_usage FLOAT NOT NULL DEFAULT 0, -- CPU占用率
    gpu_usage FLOAT NOT NULL DEFAULT 0, -- GPU占用率
    mem_usage FLOAT NOT NULL DEFAULT 0, -- 内存占用率
    record_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 业务查询索引
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