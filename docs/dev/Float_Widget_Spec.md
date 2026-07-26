# FeatherPen/docs/dev/Float_Widget_Spec.md
# GB/T 8567 V1.0.0 悬浮监控组件开发规范
## 一、组件基础约束
废弃ui/目录仅作历史规划，V1.0不实现PyQt悬浮窗口，Web端无该组件，仅桌面端预留V2.0开发规范
组件底层依赖：config_loader、member_ctrl、progress_monitor、硬件采集工具
通信规则：仅本地内存调用，不发起HTTP/api/v1请求

## 二、定时刷新国标参数
AI监控刷新：默认1秒，合法区间1~999，非法值自动回退1
硬件监控刷新：默认5秒，合法区间1~999，非法值自动回退5
配置仅在组件初始化局部加载，禁止全局常驻config变量

## 三、会员权限渲染规则
读取member_config.json权限字段：monitor_token_detail、monitor_full_data
Lv0游客全开监控面板；Lv1-Lv4分级限制；Lv5+完整开放；Lv9解锁压测数据

## 四、窗口交互标准
固定尺寸280×160；桌面支持置顶拖拽；Web/移动端禁用置顶；单例全局仅存在一个悬浮窗口
关闭按钮仅隐藏实例，不销毁后台监控定时器

## 五、跨平台启用策略
Windows/macOS/Linux：完整启用
Android/Web/小程序：隐藏入口、不实例化组件

## 六、性能强制约束
闲置无磁盘/网络IO；常驻内存上限10MB；窗口销毁同步停止所有定时任务，无内存泄漏

## 七、维护规范
组件源码统一存放ui/float_widget.py（废弃目录仅规划，V1.0不编码）
新增监控项同步更新本文档、local_member_config_v1.0.0.json权限配置