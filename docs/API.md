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
    # FeatherPen V1.0.0 API 离线接口规范文档
执行标准：GB/T 8567-2006
约束：V1.0仅本地127.0.0.1访问，无外网开放；所有接口前后端双层账号校验；统一返回JSON结构
统一返回格式：
{
  "code": int, // 200成功 / 400参数非法 / 401账号未登录 / 500服务异常
  "detail": str, // 提示文案
  "data": any // 业务返回数据，无数据时为null
}

## 基础路由前缀
/api/v1

## 一、账号用户模块 /api/v1/user
### 1. 账号格式查重接口 GET /check_name
入参：username(str) 用户名/邮箱
权限：未登录可访问（注册前置校验）
业务逻辑：查询local_user表uid字段是否存在，全局唯一校验
返回示例：
{
  "code": 200,
  "is_exist": false,
  "msg": "账号可用"
}

### 2. 账号登录校验接口 POST /login
入参：uid(str), password(str)
权限：无前置登录，后端执行双层正则校验
校验规则：
1. uid=127001 / 000000~999999 豁免通用用户名正则
2. 普通账号：6-20位 [a-zA-Z0-9_\-.]，邮箱匹配邮箱正则
3. 密码最小6位长度校验
返回：登录成功返回会员等级、积分、权限列表；失败返回400格式错误

### 3. 获取当前账号信息 GET /info
请求头：本地登录token（内存临时存储，无持久化）
返回：level、point、bind_email、bind_phone、各功能生成上限

### 4. 账号注册接口 POST /register
入参：uid、password、bind_email(可选)、bind_phone(可选)
底层约束：数据库唯一索引拦截重复邮箱/手机号，查重接口前置校验

## 二、会员积分模块 /api/v1/member
### GET /level_config
返回member_config.json完整Lv0~Lv9权限配置
### POST /point_deduct
入参：cost_type(str) 生成章节/人物/时间线等
逻辑：扣除固定积分，Lv9开启豁免开关时跳过扣减

## 三、小说AI生成模块 /api/v1/novel
### POST /gen_chapter
入参：工程名、世界设定、人物、大纲、生成章节数
权限：受会员max_output_chapter上限控制，扣除对应积分
### POST /gen_role
人物自动提取接口
### POST /gen_timeline
时间线生成接口
### POST /world_check
世界设定一致性校验（Lv0游客无权限）

## 四、本地文件快照模块 /api/v1/snapshot
### GET /list
查询当前小说工程所有快照
### POST /export
导出快照至runtime/temp
### POST /import
导入本地快照文件恢复工程

## 五、系统监控模块 /api/v1/monitor
### GET /runtime_log
读取runtime日志，自动脱敏账号密钥
### GET /token_stat
查询AI token消耗统计
### GET /progress
获取当前AI生成实时进度

## 六、系统配置模块 /api/v1/config
### GET /network_info
返回当前服务监听地址、实际端口（端口冲突自动切换后展示）
### GET /llm_model_addr
读取本地LLM推理地址127.0.0.1:1234/v1