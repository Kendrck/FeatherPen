# FeatherPen/docs/DEVELOP.md
# GB/T 8567 V1.0.0 本地开发调试规范
## 一、开发前置环境要求
Python >=3.10；系统内存≥4G；仅本地离线开发，无需云端服务
依赖安装：执行 init_env.py 自动创建虚拟环境、安装requirements.txt全部依赖

## 二、标准开发启动流程
1. 进入项目根目录
2. 执行初始化脚本：python init_env.py
   自动生成data/runtime全套四级目录、生成默认config.yaml端口配置
3. 启动程序：python main.py
   自动初始化SQLite数据库、创建十级6位测试账号、后台启动FastAPI、唤起桌面窗口

## 三、开发调试约束规则
1. 禁止修改一、二级目录，仅新增/修改三级文件
2. 代码仅保留国标业务注释，删除print调试、临时注释、草稿逻辑
3. 端口统一读取config_loader，禁止代码硬编码6554/1234
4. 账号体系严格遵循ACCOUNT_SPEC，禁止新增8位UID、云端校验逻辑
5. 所有文件增删改必须同步更新STRUCTURE.md、API_MODULE_SPEC.md
6. 废弃函数/目录/规则录入两份文档黑名单，全项目检索清理残留调用

## 四、开发调试排查方案
1. 端口占用报错：程序自动分配空闲端口，查看控制台打印实际端口
2. 数据库缺失：init_db自动执行sql_init.sql重建数据表
3. 配置文件丢失：init_env自动生成国标默认6554/1234配置
4. 导入名称报错：核对API_MODULE_SPEC函数黑名单，使用标准导出名称load_global_config/get_account_info

## 五、单元测试开发规范
1. 测试文件统一存放tests/account、tests/core/pressure
2. 测试用例仅覆盖离线账号、本地生成逻辑，不编写云端接口测试
3. 运行测试前执行init_env重置测试目录与数据库

## 六、开发交付验收标准
1. 无调试打印、无废弃注释、无残留云端/8位UID代码
2. STRUCTURE.md、API_MODULE_SPEC.md目录树、变更记录同步更新
3. 端口、函数、接口名称与基准文档完全匹配
4. 程序一键init+start无语法、导入、数据库报错