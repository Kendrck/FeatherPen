# FeatherPen/docs/dev/API_Spec.md
# GB/T 8567-2006 V1.0.0 全局RESTful接口强制规范
## 一、基础通用约束
1. 全局统一接口前缀：`/api/v1`，禁止自定义路由前缀
2. 通信协议仅本地HTTP 1.1，无HTTPS、外网接口
3. 数据格式统一UTF-8 JSON，时间标准ISO 8601
4. 同步请求：GET查询、POST提交；流式AI生成采用SSE协议

## 二、标准状态码分层
### HTTP基础状态码
200：请求正常；400参数非法；401未登录；403权限不足；404资源不存在；500服务内部异常
### 业务自定义错误码
4001：模型未加载；4002：上下文过期；4003：积分不足；4004：每日上限耗尽；4005：会员权限不足
5001：GPU显存溢出；5002：推理超时；5003：任务队列满载
### 统一异常返回模板
{
  "code": 4001,
  "message": "Model Not Loaded",
  "detail": "推理引擎模型文件缺失或损坏",
  "timestamp": "2026-07-20T14:30:00Z"
}

## 三、系统基础接口
### GET /api/v1/status
用途：前端页面初始化获取端口、版本、游客UID
入参：无
返回data：service_name、version、offline_uid、web_port（动态6554）

### POST /api/v1/user/login
用途：三层账号统一校验（127001游客/6位特权/本地注册）
请求体：{"uid":"字符串","password":"字符串"}
返回：uid、level、point、is_lv9

## 四、AI生成SSE流式接口
### POST /api/v1/generate
请求头：Content-Type:application/json; X-Session-ID会话标识
入参：prompt、context_id、stream、temperature、max_tokens
返回SSE实时文本片段，complete标识生成结束

## 五、会员与积分接口
GET /api/v1/member/info：读取当前账号权限
POST /api/v1/points/consume：扣减积分，返回变更前后余额

## 六、工程与监控接口
POST /api/v1/sync：小说工程数据本地同步
GET /api/monitor/hardware：硬件资源监控数据

## 七、接口开发强制规范
1. 所有接口实现同步写入docs/API.md归档
2. 新增接口同步更新API_MODULE_SPEC.md接口清单
3. 废弃云端cloud_login接口全文档删除，V1.0无云端业务
4. 前端api_client.js禁止硬编码端口，通过/status动态拉取web_port