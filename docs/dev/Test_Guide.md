# FeatherPen/docs/dev/Test_Guide.md
# GB/T 8567 V1.0.0 单元测试开发规范
## 一、测试框架：pytest
## 二、目录对应规则
tests/目录层级与src业务模块一一对应
tests/account → 账号校验测试
tests/core/pressure → Lv9压测专项测试

## 三、测试前置流程
执行测试前运行init_env.py重置干净目录、空数据库，避免旧数据干扰用例

## 四、必须覆盖测试范围
1. config_loader端口读取、非法值自动兜底逻辑
2. local_login账号正则校验（游客/六位特权）
3. db_sqlite.get_account_info账号查询函数
4. llm_api端口连通逻辑
5. Lv9积分豁免、压测权限拦截

## 五、禁止编写测试用例
云端8位UID、YesApi云端接口、硬件采集模块测试全部删除，V1.0无对应业务代码

## 六、CI自动化规则
.github/workflows/ci_build.yml流水线自动执行全量pytest，测试失败阻断打包发布
执行命令：pytest tests/ -v