# FeatherPen V1.0.0 代码规范

## 一、Python代码风格

### 1.1 基础规范
- 遵循 **PEP 8** 标准
- 使用 **4个空格** 缩进，禁止使用Tab
- 每行最大长度 **120字符**
- 文件末尾保留一个空行

### 1.2 命名规范
| 类型 | 规范 | 示例 |
|------|------|------|
| 模块/文件 | 小写+下划线 | `novel_auto_gen.py` |
| 类名 | 大驼峰 | `NovelAutoGenerator` |
| 函数/方法 | 小写+下划线 | `generate_next_section` |
| 变量 | 小写+下划线 | `project_path` |
| 常量 | 大写+下划线 | `MAX_RETRIES` |
| 私有成员 | 单下划线前缀 | `_load_config` |

### 1.3 注释规范
- 模块开头使用文档字符串说明功能
- 所有公共函数必须包含docstring
- 复杂逻辑处添加行内注释

## 二、项目结构规范
严格遵循 `Project_Structure.md` 定义的目录架构。

## 三、接口规范
所有API实现必须严格遵循 `API_Spec.md` 定义的接口规范。
