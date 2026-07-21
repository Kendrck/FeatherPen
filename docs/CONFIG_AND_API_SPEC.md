# 配置规范与接口定义说明书

## 1. 全局运行配置 (config.yaml)
本文件托管所有业务开关与系统参数，严禁在代码中硬编码配置项。

### 1.1 System 模块

| 字段 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| run_mode | int | 0 | 运行模式：0=生产环境, 1=调试模式, 2=沙箱测试 |
| soft_name | str | "FeatherPen" | 软件内部标识符 |
| db_secret_key | str | - | 数据库加密密钥，生产环境必须修改 |

### 1.2 Signin 模块 (登录与测试)

| 字段 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| yesapi_enable | bool | true | 是否启用 YesApi 接口服务 |
| test_account_enable | bool | true | 开启18组固定白名单测试账号 |
| lv9_skip_point_default | bool | true | Lv9 账号默认开启积分豁免 |

### 1.3 Point 模块 (积分体系)
- `daily_sign_point`: 每日签到基础积分 (默认: 100)
- `ad_reward_point`: 广告观看奖励积分 (默认: 50)

### 1.4 Monitor 模块 (监控与日志)
- `ai_monitor_refresh_sec`: AI 状态轮询间隔 (秒)
- `log_keep_days`: 日志自动清理周期 (天)

## 2. 成员配置文件 (member_config.json)
用于管理多账号体系的差异化配置。

### 2.1 数据结构
```json
{
  "members": [
    {
      "id": "user_001",
      "level": 9,
      "permissions": ["admin", "skip_verify"],
      "custom_api_key": "" 
    }
  ]
}