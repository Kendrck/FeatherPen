# FeatherPen V1.0.0 FloatMonitorWidget 悬浮监控组件开发规范

## 文档基础信息
- 文件路径：docs/dev/Float_Widget_Spec.md
- 组件源码路径：ui/float_widget.py
- 约束等级：项目强制开发标准，所有迭代必须遵循
- 关联文档：docs/dev/UI_Compatibility_Spec.md、docs/dev/Project_Structure.md

---

## 1 组件定位与依赖模块

### 1.1 组件定位
独立顶层无边框窗口，不耦合小说工作台，拥有独立UI生命周期

### 1.2 底层依赖清单
- src/config/config_loader：读取全局监控刷新配置，参数容错校验
- src/account/member_ctrl：读取会员等级与监控权限
- src/core/progress_monitor：AI章节进度、Token流量采集
- src/utils/monitor/hardware_collect：CPU/内存/GPU硬件指标采集

### 1.3 数据通信规则
仅本地内存调用底层类，不请求/api/v1系列HTTP接口，与主监控面板数据完全统一

---

## 2 定时刷新强制规范

### 2.1 AI进度/Token刷新
- 配置键：monitor.ai_monitor_refresh_sec
- 合法区间：1~999
- 非法值回滚：1秒

### 2.2 硬件资源刷新
- 配置键：monitor.hardware_monitor_refresh_sec
- 合法区间：1~999
- 非法值回滚：5秒

### 2.3 配置加载约束
配置仅在窗口__init__内部局部加载，禁止定义全局常驻配置变量

### 2.4 定时器生命周期
定时器生命周期绑定窗口，关闭自动停止，杜绝内存泄漏

---

## 3 会员权限渲染规则

权限字段严格匹配 member_config.json，通过 MemberController 统一判断：

| 权限字段 | 面板控制逻辑 |
|---------|------------|
| monitor_token_detail = false | 隐藏Token流速文本 |
| monitor_ai_progress = false | 隐藏全部AI进度面板 |
| monitor_full_data = false | 隐藏GPU占用展示 |

### 会员等级默认策略
- Lv0离线账号：全开
- Lv1~Lv4：分级限制
- Lv5及以上：全部监控开放

---

## 4 交互标准化约束

### 4.1 窗口属性
- 固定尺寸：280 × 160
- 桌面端：支持置顶、鼠标拖拽
- Web端：禁用置顶、禁用拖拽

### 4.2 交互按钮
- 右上角×按钮：仅隐藏实例，不销毁对象
- 工作台按钮：发送信号跳转创作页面

### 4.3 右键菜单
仅提供隐藏功能

### 4.4 单例控制
全局单例控制，同一时间仅存在一个悬浮窗口

---

## 5 跨平台适配规则

| 运行平台 | 启用策略 |
|---------|---------|
| Windows/Linux/macOS | 完整启用置顶、拖拽、全部监控项 |
| Android移动端 | 不实例化组件，隐藏菜单入口 |
| Web网页端 | 加载组件，永久禁用置顶、关闭拖拽 |
| 小程序端 | 移除菜单入口，完全不加载组件代码 |

### 平台检测优先级
1. WebAssembly/emscripten → web
2. Android系统 → android
3. 小程序环境 → miniprogram
4. 其他 → desktop（默认）

---

## 6 性能硬性约束

### 6.1 IO约束
闲置仅读取内存缓存，无磁盘、网络IO操作

### 6.2 内存约束
- 组件常驻内存占用上限：10MB
- 不抢占模型推理资源

### 6.3 资源释放
- 定时器随窗口关闭同步销毁线程
- 无全局配置变量，窗口销毁同步释放配置内存

---

## 7 代码维护强制规则

### 7.1 文件组织
所有悬浮窗口逻辑统一存放 ui/float_widget.py，禁止拆分多文件

### 7.2 配置规范
- 刷新时长、窗口尺寸、文案禁止硬编码，全部读取全局配置
- 配置仅在__init__局部加载，禁止定义全局config常量

### 7.3 权限规范
权限判断统一调用 MemberController，禁止手写等级判断

### 7.4 扩展规范
新增监控展示项必须同步更新本文档与 member_config.json 权限字段

---

## 8 API接口规范

### 8.1 类方法
```python
# 获取单例实例
FloatMonitorWidget.get_instance(parent=None)

# 检查单例是否存在
FloatMonitorWidget.has_instance()

# 销毁单例实例
FloatMonitorWidget.destroy_instance()

# 判断当前平台是否应显示
FloatMonitorWidget.should_show()