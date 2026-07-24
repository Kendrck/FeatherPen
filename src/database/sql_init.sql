/*
GB/T 8567-2006 国标数据库初始化脚本
项目：FeatherPen（羽笔）V1.0.0 纯离线完整版
文件路径：FeatherPen/src/database/sql_init.sql
功能：全自动数据表创建、业务索引构建、十级完整账号初始化
数据对齐：完全对标项目 member_config.json 全部账号参数
规范约束：
1. V1.0.0 纯本地离线，无云端、同步、网络字段
2. 零冗余代码，无调试/临时/废弃语句
3. 适配 TOK→GEN→CPU→GPU→MEM 五维监控标准
4. 适配五级世界树、单章5节拦截、本地积分体系
*/

-- ====================== 1. 本地离线用户账号表 ======================
-- 存储 Lv1~Lv9 完整十级离线账号，固定积分 999999999
CREATE TABLE IF NOT EXISTS local_user (
    uid CHAR(6) NOT NULL PRIMARY KEY COMMENT '6位纯数字离线账号唯一主键',
    level TINYINT NOT NULL DEFAULT 0 COMMENT '会员等级 1~9 十级离线体系',
    password VARCHAR(128) NOT NULL COMMENT '本地离线登录密码',
    point BIGINT NOT NULL DEFAULT 999999999 COMMENT '全局固定积分，所有账号统一不可修改',
    desc_text VARCHAR(256) NULL COMMENT '账号等级备注描述',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '账号创建时间戳',
    last_login_time DATETIME NULL COMMENT '最后登录时间戳',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '账号状态：0=禁用 1=正常'
) COMMENT '纯离线用户账号主表，无任何云端交互逻辑';

-- ====================== 2. 小说工程隔离表 ======================
CREATE TABLE IF NOT EXISTS novel_project (
    project_id VARCHAR(32) NOT NULL PRIMARY KEY COMMENT '小说工程唯一ID',
    uid CHAR(6) NOT NULL COMMENT '归属用户6位UID',
    book_name VARCHAR(128) NOT NULL COMMENT '自定义小说书名',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '工程创建时间',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '工程最后更新时间',
    snapshot_count INT NOT NULL DEFAULT 0 COMMENT '本地快照备份数量',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '工程状态：0=归档 1=编辑中',
    FOREIGN KEY (uid) REFERENCES local_user(uid)
) COMMENT '多小说工程独立隔离存储，防止跨工程数据污染';

-- ====================== 3. 五级世界树章节小节表 ======================
CREATE TABLE IF NOT EXISTS chapter_section (
    section_id VARCHAR(32) NOT NULL PRIMARY KEY COMMENT '小节唯一ID',
    project_id VARCHAR(32) NOT NULL COMMENT '所属工程ID',
    chapter_id VARCHAR(32) NOT NULL COMMENT '所属章节ID',
    volume_id VARCHAR(32) NOT NULL COMMENT '所属卷ID',
    section_content TEXT NULL COMMENT '小节正文内容',
    section_sort INT NOT NULL DEFAULT 0 COMMENT '小节排序序号',
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '小节生成时间',
    is_check TINYINT NOT NULL DEFAULT 0 COMMENT '剧情校正状态：0未校正 1已校正100节区间',
    FOREIGN KEY (project_id) REFERENCES novel_project(project_id)
) COMMENT '支撑五级世界树架构，适配单章5节拦截、剧情自动校正业务';

-- ====================== 4. 五维监控日志表（标准顺序TOK→GEN→CPU→GPU→MEM） ======================
CREATE TABLE IF NOT EXISTS monitor_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT COMMENT '监控日志自增主键',
    token_flow FLOAT NOT NULL DEFAULT 0 COMMENT 'TOK令牌流量消耗',
    gen_progress FLOAT NOT NULL DEFAULT 0 COMMENT 'GEN AI生成进度百分比',
    cpu_usage FLOAT NOT NULL DEFAULT 0 COMMENT 'CPU占用率',
    gpu_usage FLOAT NOT NULL DEFAULT 0 COMMENT 'GPU占用率',
    mem_usage FLOAT NOT NULL DEFAULT 0 COMMENT '内存占用率',
    record_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据采集时间戳'
) COMMENT '系统五维监控持久化存储，支撑7天自动清理日志';

-- ====================== 业务索引优化 ======================
CREATE INDEX IF NOT EXISTS idx_user_level ON local_user(level);
CREATE INDEX IF NOT EXISTS idx_project_uid ON novel_project(uid);
CREATE INDEX IF NOT EXISTS idx_section_project ON chapter_section(project_id);
CREATE INDEX IF NOT EXISTS idx_monitor_time ON monitor_record(record_time);

-- ====================== 完整十级账号初始化（100%对标配置文件） ======================
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
