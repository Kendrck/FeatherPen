# AI 模型与云端账号接口对接规范

## 1. YesApi 账号体系对接
- **基础通信协议**: HTTP GET/POST + MD5 签名验证
- **账号派发机制**: 采用"账号池"设计。所有初始账号 `account_status` 为 `pending`，通过 `App.Table.List` 接口获取后，由本地 Python 发牌官更新为 `active`。
- **昵称显示规则**: 优先读取 `ext_info.nickname`，若为空则降级显示 `username` (8位纯数字)。
- **扣费逻辑**: 9级管理员及内置 UID 跳过扣费；普通用户每小时校验 `ext_info.points`，不足则阻断服务。
