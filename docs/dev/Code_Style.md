# FeatherPen/docs/dev/Code_Style.md
# GB/T 8567 V1.0.0 Python/JS国标编码注释规范
## 一、Python 强制规范（遵循PEP8）
1. 缩进4空格，禁止Tab；单行最大120字符；文件末尾空一行
2. 文件头部国标文档注释：完整FeatherPen/文件路径、模块功能
3. 命名规则
   - 文件/函数：snake_case（小写下划线）
   - 类：PascalCase大驼峰
   - 全局常量：全大写UPPER_SNAKE
   - 私有函数/变量：单下划线_开头
4. 注释规则
   - 公共函数必须完整docstring（入参、返回、业务逻辑）
   - 删除所有print调试、#临时草稿注释、废弃代码块
   - 仅保留标准化业务说明，无个人待办、迭代备注
5. 模块导出：公共函数统一写入`__all__`，禁止随意import暴露内部方法

## 二、前端 JS/HTML/CSS 规范
1. 编码统一UTF-8无BOM，缩进2空格
2. 全局账号、端口常量统一存放api_client.js，页面禁止重复定义
3 删除console.log调试语句，页面无硬编码中文文本（i18n读取）
4 CSS全局样式统一main.css，页面禁止重复样式代码

## 三、文档统一约束
所有.md、py、js仅保留国标业务注释；
新增代码、修改函数名/端口/接口，同步更新STRUCTURE.md、API_MODULE_SPEC.md。

## 四、废弃命名黑名单（全项目禁用）
load_config（标准load_global_config）
db_get_user_info（标准get_account_info）
8位UID全套账号逻辑
硬编码6554/1234数字
ui/electron旧界面相关代码