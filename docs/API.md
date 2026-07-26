# FeatherPen/docs/API.md
# GB/T 8567 V1.0.0 离线HTTP接口完整规范
全局统一API基准前缀：/api/v1
全局标准返回JSON结构：
{
  "code": int,
  "detail": str,
  "data": any|null
}
统一错误码：200成功、400参数非法、401账号校验失败、403权限不足、500服务异常

## 一、系统基础接口
### GET /api/v1/status
用途：页面初始化拉取端口、版本、离线游客UID
入参：无
返回data：service_name、version、offline_uid、web_port

## 二、账号用户模块（纯离线，废弃云端cloud_login）
### POST /api/v1/user/login
用途：三层账号统一校验（游客/6位特权/本地注册账号）
Content-Type: application/json
请求体 {"uid":"字符串","password":"字符串"}
业务流程：前端校验 → 后端二次正则校验 → 匹配特权账号/数据库账号
成功返回data：uid、level、current_point、is_lv

### GET /api/v1/user/check_name
用途：注册前置账号/邮箱查重
入参：username
返回is_exist布尔值

### GET /api/v1/user/info
用途：获取当前登录账号完整会员权限配置

### POST /api/v1/user/register
用途：本地新建账号，底层唯一索引拦截重复邮箱/手机号

## 三、会员积分模块
### GET /api/v1/member/level_config
读取完整Lv0~Lv9权限配置
### POST /api/v1/member/toggle_lv9_deduct
仅Lv9账号可用，切换积分豁免开关并持久化至member_config.json

## 四、AI小说生成模块
### POST /api/v1/novel/gen_chapter
生成章节，自动判断Lv9豁免开关是否扣减积分
### POST /api/v1/novel/gen_role
人物自动提取接口
### POST /api/v1/novel/gen_timeline
时间线生成接口
### POST /api/v1/novel/world_check
世界观一致性校验（Lv0游客无权限）

## 五、工程快照模块
### GET /api/v1/snapshot/list
查询当前工程所有快照
### POST /api/v1/snapshot/export
导出快照至runtime/temp
### POST /api/v1/snapshot/import
恢复本地快照文件

## 六、系统监控模块
### GET /api/monitor/hardware
硬件监控数据
### GET /api/monitor/token_stat
Token消耗统计
### GET /api/monitor/progress
AI实时生成进度

## 七、系统配置模块
### GET /api/config/network_info
返回当前实际监听端口、LLM推理地址127.0.0.1:1234

## 永久废弃接口
POST /api/v1/account/cloud_login 云端登录接口（V1.0不编码实现，文档全量删除）