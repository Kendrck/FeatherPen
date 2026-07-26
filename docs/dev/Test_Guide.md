# FeatherPen/docs/dev/Test_Guide.md
# GB/T 8567 V1.0.0 单元测试国标规范
## 一、测试运行框架：pytest
## 二、测试目录与业务映射
tests/account → 账号常量、特权UID白名单权限校验用例
tests/core/pressure → 压测功能权限拦截专项用例
## 三、测试前置标准化流程
执行任意测试集前运行init_env.py，重置干净目录、空SQLite数据库，避免脏数据干扰用例执行结果
## 四、强制全覆盖测试用例清单
1. config_loader端口读取、非法数值回落逻辑；严格区分Web自动分配、LLM 1234固定两套规则
2. local_login前后端常量一致性校验：OFFLINE_GUEST_UID、PRIVILEGE_UID_LIST必须完全匹配
3. db_sqlite.get_account_info账号查询接口正确性校验
4. ll_api 1234端口连通性功能测试
5. 权限隔离核心强制用例：仅Lv9、不在白名单的账号，调用积分开关、压测接口，服务必须返回403权限不足
## 五、禁止编写测试用例范围
云端8位UID、YesApi对接、硬件采集相关测试全部删除，V1.0无对应落地业务代码
## 六、CI自动化规范
.github/workflows/ci_build.yml流水线自动执行全量pytest，测试失败阻断打包发布流程
标准执行命令：pytest tests/ -v