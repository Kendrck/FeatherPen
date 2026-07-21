# FeatherPen/ui/float_widget.py
"""
FeatherPen V1.0.0 悬浮监控顶层窗口 FloatMonitorWidget
规范对齐 docs/dev/Float_Widget_Spec.md：
1. 独立无边框顶层窗口，无工作台页面耦合，独立UI生命周期
2. 配置仅在__init__局部加载，无全局常驻变量，配置损坏自动兜底默认值
3. 联动MemberController动态控制监控面板显隐，严格匹配member_config.json权限
4. 复用ProgressMonitor、HardwareCollector全局采集类，不重复创建采集逻辑
5. Qt信号槽解耦主窗口，禁止跨文件直接调用实例方法
6. 多平台自动降级：Android/Web/小程序自动关闭置顶/隐藏入口
7. 定时器随窗口销毁释放，常驻内存≤10MB，闲置无磁盘、网络高频IO
8. 内置单例静态方法，全局唯一悬浮实例，防止多窗口资源冲突
"""
import sys
import platform
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QMenu
)
from PyQt6.QtCore import Qt, QTimer, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QAction

# 项目标准化内部模块导入
from src.config.config_loader import ConfigLoader
from src.core.progress_monitor import ProgressMonitor
from src.utils.monitor.hardware_collect import HardwareCollector
from src.account.member_ctrl import MemberController


class FloatMonitorWidget(QWidget):
    """
    全局悬浮监控窗口：实时展示AI生成进度、Token流速、CPU/内存/GPU占用
    全局单例控制，同一时间仅存在一个悬浮窗口实例
    """
    # 对外交互信号（窗口→主窗口通信，解耦无直接调用）
    jump_workbench_signal = pyqtSignal()
    close_float_signal = pyqtSignal()

    # 静态单例缓存
    _instance = None

    @classmethod
    def get_instance(cls, parent=None):
        """静态方法：获取/创建全局唯一悬浮窗实例"""
        if cls._instance is None:
            cls._instance = cls(parent)
        return cls._instance

    @classmethod
    def has_instance(cls):
        """静态方法：判断单例是否已创建"""
        return cls._instance is not None

    @classmethod
    def destroy_instance(cls):
        """静态方法：销毁并清空单例"""
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None

    def __init__(self, parent=None):
        # 单例防重复实例化保护
        if FloatMonitorWidget._instance is not None:
            raise RuntimeError("FloatMonitorWidget 为全局单例组件，请调用get_instance()获取")
        super().__init__(parent)

        # 局部加载配置（规范强制：禁止全局配置变量，异常自动兜底默认刷新时长）
        try:
            config = ConfigLoader().load_full_config()
            ai_refresh_raw = config["monitor"]["ai_monitor_refresh_sec"]
            self._ai_refresh_sec = ai_refresh_raw if 1 <= ai_refresh_raw <= 999 else 1
            hw_refresh_raw = config["monitor"]["hardware_monitor_refresh_sec"]
            self._hw_refresh_sec = hw_refresh_raw if 1 <= hw_refresh_raw <= 999 else 5
        except Exception:
            # 配置文件缺失/损坏，使用文档标准默认值
            self._ai_refresh_sec = 1
            self._hw_refresh_sec = 5

        # 运行平台识别
        self._platform = self._detect_platform()
        # 根据平台生成窗口置顶属性
        self.setWindowFlags(self._get_window_flags())
        # 窗口固定标准尺寸
        self.setFixedSize(280, 160)
        # 跨平台统一半透明深色样式，无专属字体硬编码
        self.setStyleSheet("""
            QWidget {background-color: rgba(30,30,36,230); color:#f0f0f0; border-radius:8px;}
            QLabel {font-size:12px; padding:2px;}
            QPushButton {background:#3a3a48; border:none; border-radius:4px; padding:4px; font-size:11px;}
            QPushButton:hover {background:#505068;}
        """)

        # 鼠标拖拽缓存坐标
        self._drag_start_pos = QPoint()
        self._window_start_pos = QPoint()

        # 底层业务采集、权限控制实例
        self._member_ctrl = MemberController()
        self._progress_monitor = ProgressMonitor()
        self._hw_collector = HardwareCollector()

        # 数据刷新定时器（绑定实例生命周期，关闭自动停止）
        self._timer_ai = QTimer(self)
        self._timer_ai.setInterval(self._ai_refresh_sec * 1000)
        self._timer_ai.timeout.connect(self._refresh_ai_data)

        self._timer_hw = QTimer(self)
        self._timer_hw.setInterval(self._hw_refresh_sec * 1000)
        self._timer_hw.timeout.connect(self._refresh_hardware_data)

        # 初始化全部UI布局
        self._init_ui_layout()
        # 写入单例静态缓存
        FloatMonitorWidget._instance = self
        # 根据会员权限初始化面板显隐
        self._update_view_by_member_level()
        # 启动定时数据刷新
        self._timer_ai.start()
        self._timer_hw.start()

    def _detect_platform(self):
        """识别当前运行平台，返回 desktop/android/web/miniprogram"""
        if platform.system() == "Android" or "android" in platform.platform().lower():
            return "android"
        if hasattr(sys, "platform") and "emscripten" in sys.platform:
            return "web"
        if "MINIPROGRAM" in sys.modules or "wx" in sys.modules:
            return "miniprogram"
        return "desktop"

    def _get_window_flags(self):
        """根据平台切换置顶开关，Web/移动端禁用置顶"""
        if self._platform == "web":
            return Qt.WindowType.FramelessWindowHint
        return Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint

    @classmethod
    def should_show(cls):
        """供主窗口调用：判断当前平台是否允许展示悬浮窗"""
        if hasattr(sys, "platform") and "emscripten" in sys.platform:
            return False
        if platform.system() == "Android" or "android" in platform.platform().lower():
            return False
        if "MINIPROGRAM" in sys.modules or "wx" in sys.modules:
            return False
        return True

    def _init_ui_layout(self):
        """分层构建UI：标题栏、AI进度面板、硬件监控面板"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(6)

        # 顶部标题与操作按钮
        title_layout = QHBoxLayout()
        self._label_title = QLabel("羽笔·悬浮监控")
        self._label_title.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
        self._btn_jump = QPushButton("工作台")
        self._btn_jump.clicked.connect(self.jump_workbench_signal.emit)
        self._btn_close = QPushButton("×")
        self._btn_close.setFixedWidth(24)
        self._btn_close.clicked.connect(self._on_close_clicked)

        title_layout.addWidget(self._label_title)
        title_layout.addStretch(1)
        title_layout.addWidget(self._btn_jump)
        title_layout.addWidget(self._btn_close)

        # AI生成进度面板容器
        self._frame_ai = QFrame()
        layout_ai = QVBoxLayout(self._frame_ai)
        layout_ai.setContentsMargins(4, 4, 4, 4)
        layout_ai.setSpacing(2)
        self._label_ai_title = QLabel("【生成进度】")
        self._label_ai_progress = QLabel("当前无生成任务")
        self._label_token = QLabel("Token流速：0 tok/s")
        layout_ai.addWidget(self._label_ai_title)
        layout_ai.addWidget(self._label_ai_progress)
        layout_ai.addWidget(self._label_token)

        # 硬件监控面板容器
        self._frame_hw = QFrame()
        layout_hw = QVBoxLayout(self._frame_hw)
        layout_hw.setContentsMargins(4, 4, 4, 4)
        layout_hw.setSpacing(2)
        self._label_hw_title = QLabel("【硬件占用】")
        self._label_cpu = QLabel("CPU：0%")
        self._label_mem = QLabel("内存：0MB")
        self._label_gpu = QLabel("GPU：未检测")
        layout_hw.addWidget(self._label_hw_title)
        layout_hw.addWidget(self._label_cpu)
        layout_hw.addWidget(self._label_mem)
        layout_hw.addWidget(self._label_gpu)

        # 组装总布局
        main_layout.addLayout(title_layout)
        main_layout.addWidget(self._frame_ai)
        main_layout.addWidget(self._frame_hw)
        self.setLayout(main_layout)

    def _update_view_by_member_level(self):
        """读取会员权限配置，自动隐藏无权限监控模块"""
        level_info = self._member_ctrl.get_current_level_info()
        self._frame_ai.setVisible(level_info.get("monitor_ai_progress", True))
        self._label_token.setVisible(level_info.get("monitor_token_detail", True))
        self._label_gpu.setVisible(level_info.get("monitor_full_data", True))

    def _refresh_ai_data(self):
        """刷新AI章节进度、实时Token流速，复用全局监控数据"""
        progress_data = self._progress_monitor.get_current_progress()
        token_data = self._progress_monitor.get_token_flow()
        if progress_data.get("running", False):
            chap = progress_data.get("current_chap", "未知")
            remain = progress_data.get("remain_sec", 0)
            self._label_ai_progress.setText(f"章节：{chap} | 剩余：{remain}s")
        else:
            self._label_ai_progress.setText("当前无生成任务")
        self._label_token.setText(f"Token流速：{token_data.get('speed', 0)} tok/s")

    def _refresh_hardware_data(self):
        """采集并渲染CPU/内存/GPU硬件占用指标"""
        hw_data = self._hw_collector.get_all_hardware_info()
        self._label_cpu.setText(f"CPU：{hw_data.get('cpu_usage', 0)}%")
        self._label_mem.setText(f"内存：{hw_data.get('mem_mb', 0)}MB")
        if hw_data.get("gpu_support", False):
            gpu_usage = hw_data.get("gpu_usage", 0)
            gpu_vram = hw_data.get("gpu_vram", 0)
            self._label_gpu.setText(f"GPU：{gpu_usage}% | 显存：{gpu_vram}MB")
        else:
            self._label_gpu.setText("GPU：无显卡设备")

    def _on_close_clicked(self):
        """关闭按钮统一处理：仅隐藏不销毁实例"""
        self.hide()
        self.close_float_signal.emit()

    def mousePressEvent(self, event):
        """鼠标左键按下，缓存拖拽起点；Web端禁用拖拽"""
        if self._platform == "web":
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.globalPosition().toPoint()
            self._window_start_pos = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """拖拽移动窗口，Web端不生效"""
        if self._platform == "web" or self._drag_start_pos.isNull():
            return
        delta = event.globalPosition().toPoint() - self._drag_start_pos
        self.move(self._window_start_pos + delta)

    def contextMenuEvent(self, event):
        """右键上下文菜单：仅隐藏功能"""
        menu = QMenu(self)
        act_hide = QAction("隐藏悬浮监控窗", self)
        act_hide.triggered.connect(self._on_close_clicked)
        menu.addAction(act_hide)
        menu.exec(event.globalPos())

    def closeEvent(self, event):
        """窗口销毁回调：停止定时器、清空单例、释放资源防泄漏"""
        self._timer_ai.stop()
        self._timer_hw.stop()
        if FloatMonitorWidget._instance is self:
            FloatMonitorWidget._instance = None
        super().closeEvent(event)

    def show_float(self):
        """对外展示接口：平台校验后显示"""
        if self.should_show():
            self.show()
        else:
            import warnings
            warnings.warn(f"当前平台 {self._platform} 不支持悬浮监控窗口")

    def toggle_visibility(self):
        """切换窗口显示/隐藏，供主窗口菜单调用"""
        if self.isVisible():
            self.hide()
        else:
            self.show_float()