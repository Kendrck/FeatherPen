# FeatherPen/docs/API.md
# GB/T 8567 V1.0.0 离线HTTP接口国标规范
全局统一API基准前缀：/api/v1
标准返回JSON结构：
{
  "code": int,
  "detail": str,
  "data": any|null
}
统一错误码定义：
200 请求成功
400 请求参数非法
401 账号密码校验失败
403 权限不足（细分：等级不足 / 非特权UID白名单调用积分/压测专属接口）
500 服务内部异常
## 一、系统基础接口
### GET /api/v1/status
用途：页面初始化获取运行端口、程序版本、游客UID
入参：无
返回data：service_name、version、offline_uid、web_port
## 二、账号用户模块（纯离线，废弃云端登录接口）
### POST /api/v1/user/login
用途：三层账号统一校验（游客/普通注册账号/特权UID白名单账号）
Content-Type: application/json
请求体 {"uid":"字符串","password":"字符串"}
执行流程：前端格式校验 → 后端二次正则校验 → 匹配数据库/预置白名单账号
成功返回：uid、level、current_point、is_lv
### GET /api/v1/user/check_name
用途：注册账号/邮箱查重
入参：username
返回布尔值is_exist
### GET /api/v1/user/info
用途：获取当前登录账号完整会员权限配置
### POST /api/v1/user/register
用途：本地新建普通账号，数据库唯一索引拦截重复邮箱、账号
## 三、会员积分模块
### GET /api/v1/member/level_config
用途：读取全套Lv0~Lv9会员等级配置参数
### POST /api/v1/member/toggle_lv9_deduct
权限限制：仅特权UID白名单账号可调用；纯Lv9标准账号请求返回403；功能为切换积分豁免开关并持久写入member_config.json
## 四、AI小说生成模块
### POST /api/v1/novel/gen_chapter
生成章节接口，自动校验当前UID是否在白名单，判定是否扣减积分
### POST /api/v1/novel/gen_role
人物自动提取接口
### POST /api/v1/novel/gen_timeline
故事时间线生成接口
### POST /api/v1/novel/world_check
世界观一致性校验，Lv0游客无访问权限
## 五、工程快照模块
### GET /api/v1/snapshot/list
查询当前小说工程全部快照
### POST /api/v1/snapshot/export
导出快照至runtime/temp临时目录
### POST /api/v1/snapshot/import
本地快照文件恢复工程数据
## 六、系统监控模块
### GET /api/monitor/hardware
硬件资源实时数据
### GET /api/monitor/token_stat
Token消耗统计数据
### GET /api/monitor/progress
AI生成实时进度
## 七、系统配置模块
### GET /api/config/network_info
返回当前Web监听端口、LLM推理固定地址127.0.0.1:1234
## 永久废弃接口
POST /api/v1/account/cloud_login 云端登录接口（V1.0无任何落地代码，全文档删除相关描述）