# FeatherPen - 数据库与持久化规范 (V1.0.0)

## 1. 数据库引擎
- **类型**: SQLite 3
- **文件位置**: `data/featherpen.db`
- **连接模式**: WAL (Write-Ahead Logging) 以支持并发读取

## 2. 核心表结构定义

### 2.1 `accounts` (账号管理表)
存储所有登录账号的基础信息与状态。

| 字段名 | 类型 | 约束 | 说明 |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 唯一标识符 |
| `username` | TEXT | UNIQUE NOT NULL | 登录用户名 |
| `password_hash` | TEXT | NOT NULL | 加密后的密码哈希值 |
| `level` | INTEGER | DEFAULT 1 | 账号等级 (1-9) |
| `is_vip` | BOOLEAN | DEFAULT FALSE | 是否为 VIP 账号 |
| `status` | TEXT | DEFAULT 'active' | 状态: active, banned, expired |
| `last_login` | DATETIME | - | 最后登录时间戳 |

### 2.2 `points_log` (积分流水表)
记录所有积分变动，用于审计与回放。

| 字段名 | 类型 | 约束 | 说明 |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | 流水ID |
| `account_id` | INTEGER | FOREIGN KEY | 关联 accounts.id |
| `change_amount` | INTEGER | NOT NULL | 变动数值 (+/-) |
| `type` | TEXT | NOT NULL | 类型: sign_in, ad_reward, consume |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | 发生时间 |

## 3. 索引规范
- `idx_accounts_username`: 加速用户名查询
- `idx_points_account_time`: 加速积分流水按账号+时间查询

## 4. 迁移策略
- 所有表结构变更必须通过 `src/db/migrations/` 下的 SQL 脚本执行。
- 禁止直接在代码中硬编码 `CREATE TABLE` 语句。