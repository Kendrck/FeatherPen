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

# API 接口定义说明书 (V1.0.0)

## 1. 账户模块 (Account)

### 1.1 云端登录
- **接口**: `POST /api/v1/account/cloud_login`
- **描述**: 统一登录入口，自动识别白名单测试账号。
- **请求参数**:
    ```json
    {
      "username": "11111111",  // UID
      "password": "admin...",  // MD5加密后的密码
      "login_type": "cloud"
    }

    ```
- **响应字段**:
    ```json
    {
      "code": 0,
      "data": {
        "token": "xxx",
        "ext_info": { "level": 9, "level_name": "Lv9 不朽" },
        "is_test_account": true,       // 是否为测试账号
        "is_lv9_privilege": true,      // 是否拥有Lv9特权
        "current_deduct_switch": true  // 当前积分豁免状态
      }
    }

    ```

### 1.2 切换 Lv9 积分豁免
- **接口**: `POST /api/v1/account/toggle_lv9_deduct`
- **描述**: 仅 Lv9 账号可用，切换积分扣除开关。
- **请求参数**:
    ```json
    {
      "enable_skip": true  // true=开启豁免(不扣费), false=关闭豁免(扣费)
    }

    ```
- **逻辑**: 修改全局配置 `cloud_privilege.skip_point_deduct` 并持久化。

## 2. 生成模块 (Generate)

### 2.1 内容生成扣费判定
- **逻辑**: 在 `/api/v1/generate` 内部执行。
- **伪代码**:
    ```python
    if user.uid in ["99999999", "00000000"] and config.skip_point_deduct:
        # Lv9 且开启豁免，跳过扣费
        pass
    else:
        # 正常扣费
        point_system.deduct(type="gen_chapter")

    ```