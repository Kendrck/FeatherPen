# API.md 后端接口完整规范 V1.0.0
全局接口前缀：/api/v1/
AI生成接口强制SSE流式输出

## 1. 账号登录接口
### POST /api/v1/account/cloud_login
入参：
- username: str 8位UID
- password: str MD5加密密码
- login_type: int 0离线/1云端

返回体：
```json
{
  "code": 200,
  "msg": "登录成功",
  "ext_info": {},
  "is_test_account": true,
  "is_lv9_privilege": true,
  "current_deduct_switch": true
}