# Feather 羽笔 V1.0.0
## 项目定位 GB/T 8567 纯离线本地AI小说创作工具
仅127.0.0.1本地回环通信，无外网请求、云端存储、云端算力，用户数据本地隔离保存
## 技术栈
Python3.10+ / FastAPI / PyWebView / 原生HTML/CSS/JS / SQLite
永久废弃：Electron、PyQt6图形框架，无相关业务代码与打包流程
## 核心业务规则
1. Lv0离线游客固定UID=127001，免注册、免账号格式校验
2. 内置10组特权UID白名单账号分级开放基础生成、监控权限；Lv9仅扩容章节上限
3. 积分豁免、无上限批量生成、压测功能仅特权UID白名单账号拥有，纯Lv9标准账号不具备该类特权
4. 支持世界观、人物、大纲、章节全自动AI生成
5. 小说工程四级分层存储：db库、章节文本、向量缓存、快照备份
6. 端口容错规范：Web默认6554，占用自动分配空闲端口；LLM推理端口固定1234，不自动切换
## 内置特权白名单账号（统一密码passwd）
|会员等级 | 6位UID | 权限说明 |
| Lv1 | 111111 | 特权UID白名单账号，自带积分豁免、压测权限，等级仅小幅扩容生成上限 |
| Lv2 | 222222 | 特权UID白名单账号，自带积分豁免、压测权限，等级仅小幅扩容生成上限 |
| Lv3 | 333333 | 特权UID白名单账号，自带积分豁免、压测权限，等级仅小幅扩容生成上限 |
| Lv4 | 444444 | 特权UID白名单账号，自带积分豁免、压测权限，等级仅小幅扩容生成上限 |
| Lv5 | 555555 | 特权UID白名单账号，自带积分豁免、压测权限，等级仅小幅扩容生成上限 |
| Lv6 | 666666 | 特权UID白名单账号，自带积分豁免、压测权限，等级仅小幅扩容生成上限 |
| Lv7 | 777777 | 特权UID白名单账号，自带积分豁免、压测权限，等级仅小幅扩容生成上限 |
| Lv8 | 888888 | 特权UID白名单账号，自带积分豁免、压测权限，等级仅小幅扩容生成上限 |
| Lv9 | 999999 | 特权UID白名单账号，无生成数量上限，自带积分豁免、压测权限 |
| Lv9 | 000000 | 特权UID白名单账号，无生成数量上限，自带积分豁免、压测权限 |
## 标准启动命令
1. 初始化运行目录、生成标准端口配置
python init_env.py
2. 启动桌面客户端
python main.py
## docs规范文档索引
### 架构基准文档
STRUCTURE.md 项目三级目录世界树归档文档
API_MODULE_SPEC.md 端口、函数、接口全局基准规范
API.md HTTP完整接口手册
ACCOUNT_SPEC.md 账号三层校验国标规范
CONFIG_AND_API_SPEC.md 端口通信配置细则
DATABASE_SCHEMA.md SQLite数据表规范
COMPATIBILITY.md 跨平台兼容规范
DEPLOYMENT_GUIDE.md 打包部署操作指南
PROJECT_OVERVIEW.md 离线隐私整体说明
DEVELOP.md 本地开发调试规范
PRESS_TEST.md 特权UID压测功能规范
local_member_config_v1.0.0.json 会员权限标准配置模板
### 开发细则文档
dev/Project_Structure.md 目录层级解读
dev/UI_Compatibility_Spec.md 前端跨端兼容
dev/Code_Style.md 编码注释国标
dev/Test_Guide.md 单元测试规范
dev/Build_Guide Windows打包说明
### 用户操作文档
user/Install_Guide.md 安装教程
user/Language_Spec.md 多语言配置
user/Data_Import_Export.md 工程导入导出
user/FAQ.md 端口、登录报错解决方案
## 全局强制约束
1. 一、二级目录锁定不可修改，仅拓展三级文件/子目录
2. 全部服务仅监听127.0.0.1，禁止0.0.0.0公网监听
3. 前后端代码禁止硬编码6554、1234端口，统一读取配置文件
4. 账号体系仅保留127001游客+6位特权UID白名单，8位云端账号全量废弃
5. 端口区分规则：Web端口6554占用自动分配；LLM端口1234固定不切换
6. 任何文件、接口、端口修改必须同步更新STRUCTURE.md、API_MODULE_SPEC.md两份归档文档