# YESAPI_ACCOUNT.md 云端白名单账号对接规范 V1.0.0
## 1. 账号基础规则
1. 预置10组固定8位UID白名单账号，密码统一为administrator
2. 不独立开辟测试登录页面，复用统一云端登录弹窗，内置快捷填充按钮
3. 仅UID=99999999、00000000为Lv9不朽特权账号，支持积分豁免开关

## 2. 账号等级对应UID
|等级|UID|权限说明|
|----|----|----|
|Lv1|11111111|基础生成权限|
|Lv2|22222222|开放5章节生成上限|
|Lv3|33333333|开放AI进度监控|
|Lv4|44444444|50章节上限|
|Lv5|55555555|完整监控面板|
|Lv6|66666666|200章节上限|
|Lv7|77777777|500章节上限|
|Lv8|88888888|1000章节上限|
|Lv9|99999999|无上限、积分豁免开关|
|Lv9|00000000|无上限、积分豁免开关|

## 3. 登录接口统一规范
接口地址：/api/v1/account/cloud_login
请求参数：username(UID)、password(MD5加密)、login_type
返回标识：is_test_account、is_lv9_privilege、current_deduct_switch

## 4. Lv9扣费开关接口
POST /api/v1/account/toggle_lv9_deduct
入参：enable_skip: bool
作用：全局持久化积分豁免状态，全界面实时同步

## 5. 积分扣费判定逻辑
仅Lv9两个白名单账号受skip_point_deduct配置控制；其余账号固定扣除对应积分。