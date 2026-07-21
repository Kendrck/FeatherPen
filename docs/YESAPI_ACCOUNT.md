# YESAPI_ACCOUNT.md 云端测试账号对接规范 V1.0.0
## 1. 固定10组白名单测试账号（不可修改）
|等级|UID|默认密码|特权说明|
|----|----|----|----|
|Lv1|11111111|administrator|基础测试账号|
|Lv2|22222222|administrator|小幅提升创作上限|
|Lv3|33333333|administrator|开放AI进度监控|
|Lv4|44444444|administrator|50章节生成上限|
|Lv5|55555555|administrator|完整硬件监控|
|Lv6|66666666|administrator|200章节上限|
|Lv7|77777777|administrator|500章节上限|
|Lv8|88888888|administrator|1000章节上限|
|Lv9|99999999|administrator|不朽特权，积分豁免开关控制|
|Lv9|00000000|administrator|不朽特权，积分豁免开关控制|

## 2. 登录约束
1. 无独立测试登录页面，复用统一云端登录弹窗
2. 弹窗内置10个快捷填充按钮，一键填充UID+默认密码
3. 登录接口统一：POST /api/v1/account/cloud_login

## 3. Lv9特权规则
1. 仅两个Lv9 UID触发积分豁免逻辑
2. 全局开关托管member_config.json cloud_privilege.skip_point_deduct
3. 前端会员面板仅登录Lv9账号展示开关控件与状态提示

## 4. 权限下发逻辑
登录校验匹配白名单UID后，返回字段：
- is_test_account: bool 是否测试账号
- is_lv9_privilege: bool 是否Lv9特权账号
- current_deduct_switch: bool 当前积分豁免开关状态      