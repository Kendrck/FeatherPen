# FeatherPen 账号与会员体系规范

## 1. 账号格式
- 统一采用 8 位纯数字 UID，由系统自动派发，用户不可修改。
- 初始密码统一为 `123456`，首次登录强制要求修改。

## 2. 等级定义 (ext_info.level)
- `0`: 离线/未激活状态
- `1-8`: 普通用户等级
- `9`: 管理员/开发测试账户 (拥有永久特权，不扣积分)

## 3. 核心扩展字段 (ext_info)
- `nickname`: 用户自定义昵称
- `level`: 会员等级
- `points`: 当前积分余额
- `account_status`: `pending` (待派发) / `active` (已激活)
- `vip_expire_time`: 会员过期时间戳
- `bind_token`: 并发抢号防重令牌
