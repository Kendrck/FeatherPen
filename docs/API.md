# API.md FeatherPen后端接口规范 V1.0.0
## 全局统一约束
1. 所有接口前缀统一：/api/v1/
2. AI生成接口强制SSE流式返回
3. 所有接口返回标准JSON结构

## 1. 账号登录接口
### POST /api/v1/account/cloud_login
入参：
- username: str 8位UID
- password: str MD5加密密码
- login_type: int 登录模式标识
返回字段：
- ext_info: dict 会员等级原始信息
- is_test_account: bool 是否白名单测试账号
- is_lv9_privilege: bool 是否Lv9特权账号
- current_deduct_switch: bool 当前积分豁免开关状态

## 2. Lv9积分开关控制接口
### POST /api/v1/account/toggle_lv9_deduct
入参：
- enable_skip: bool true=开启积分豁免 false=关闭豁免
功能：持久化更新member_config.json中cloud_privilege.skip_point_deduct，全端实时生效

## 3. AI小说生成扣费逻辑
生成章节前校验：
1. 判断当前登录UID是否属于lv9_uid_list
2. 读取全局skip_point_deduct开关
3. 双条件同时成立则跳过积分扣除，其余场景正常扣费