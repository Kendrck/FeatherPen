# FeatherPen/docs/dev/Test_Guide.md
# GB/T 8567 V1.0.0 单元测试国标规范
## 一、测试运行框架：pytest
## 二、测试目录与业务映射
tests/account → 账号常量、特权UID白名单权限校验用例
tests/core/pressure → 压测功能权限拦截专项用例
## 三、测试前置标准化流程
执行任意测试集前运行init_env.py，重置干净目录、空SQLite库，避免脏数据干扰
## 四、强制全覆盖测试用例清单
1. config_loader端口读取、非法数值回落逻辑；区分Web自动分配、LLM固定1234两套规则
2. local_login前后端常量一致性校验（OFFLINE_GUEST_UID、PRIVILEGE_UID_LIST完全匹配）
3. db_sqlite.get_account_info账号查询函数正确性
4. llm_api 1234端口连通性测试
5. 权限隔离核心用例：仅Lv9但不在白名单的账号，调用积分开关、压测接口必须返回403权限不足
## 五、禁止编写测试用例范围
云端8位UID、YesApi对接、硬件采集相关测试全部删除，V1.0无落地代码
## 六、CI自动化规范
.github/workflows/ci_build.yml流水线自动执行全量pytest，测试失败阻断打包发布
标准执行命令：pytest tests/ -v