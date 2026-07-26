# FeatherPen 羽笔 V1.0.0
## 项目定位 GB/T 8567 纯离线本地AI小说创作工具
全程仅127.0.0.1本地内网通信，无外网、云端同步、硬件采集逻辑，保护本地隐私。

## 技术栈
Python3.10+ / FastAPI / PyWebView / 原生HTML/CSS/JS / SQLite
永久废弃：Electron、PyQt6图形界面框架

## 核心功能
1. Lv0离线游客：固定UID=127001，免注册、免格式校验直接创作
2. Lv1~Lv9六级本地特权账号，分级小说生成上限、AI监控权限
3. Lv9不朽特权：积分豁免开关、无章节生成上限、压测功能
4. 世界设定、人物、大纲、章节AI自动生成
5. 小说工程四级分层存储：db/章节/向量缓存/快照备份
6. 端口自动容错：6554占用自动切换空闲端口，对接LM Studio推理端口1234

## 本地内置特权账号（统一密码 passwd）
|等级 | 6位UID | 权限说明 |
| Lv1 | 111111 | 基础创作权限 |
| Lv2 | 222222 | 小幅提升章节上限 |
| Lv3 | 333333 | 开放人物/时间线生成 |
| Lv4 | 444444 | 批量导出章节权限 |
| Lv5 | 555555 | 完整世界观校验 |
| Lv6 | 666666 | 扩大章节生成上限 |
| Lv7 | 777777 | 全监控面板开放 |
| Lv8 | 888888 | 民用满级常规权限 |
| Lv9 | 999999 | 不朽特权，积分豁免开关 |
| Lv9 | 000000 | 不朽特权，积分豁免开关 |

## 快速启动命令
1. 初始化运行目录、默认配置
python init_env.py
2. 启动桌面客户端
python main.py

## docs 完整文档索引
### 架构&基准规范
STRUCTURE.md 项目三级世界树总架构
API_MODULE_SPEC.md 端口/函数/接口全局唯一基准
API.md 离线HTTP接口完整手册
ACCOUNT_SPEC.md Lv0-Lv9三层账号校验国标
CONFIG_AND_API_SPEC.md 网络端口配置细则
DATABASE_SCHEMA.md SQLite数据表规范
COMPATIBILITY.md 全平台兼容规范
DEPLOYMENT_GUIDE.md 打包部署操作指南
PROJECT_OVERVIEW.md 项目离线隐私说明
DEVELOP.md 本地开发调试指南
PRESS_TEST.md Lv9压测解锁规范
local_member_config_v1.0.0.json 会员权限标准模板

### dev 开发细则文档
Project_Structure.md 目录层级解读
UI_Compatibility_Spec.md Web前端兼容
Code_Style.md 国标代码注释规范
Test_Guide.md 单元测试编写
Build_Guide Windows打包脚本说明

### user 用户操作手册
Install_Guide.md 安装教程
Language_Spec.md 多语言配置
Data_Import_Export.md 小说工程导入导出
FAQ.md 端口占用、登录报错解决方案

## 全局硬性约束
1. 一、二级目录固定不可修改，仅三级拓展文件/子目录
2. 所有服务仅绑定127.0.0.1，禁止0.0.0.0公网监听
3. 后端/前端禁止硬编码6554、1234端口数字，统一配置读取
4. 账号体系仅保留127001游客+6位数字特权，8位云端账号规则全部废弃
5. 任何代码修改必须同步更新STRUCTURE.md、API_MODULE_SPEC.md归档