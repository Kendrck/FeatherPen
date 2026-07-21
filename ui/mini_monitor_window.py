# FeatherPen V1.0.0 迷你监控悬浮小窗口
# 文件路径：FeatherPen/src/ui/mini_monitor_window.py
# 规范遵循：PyQt6界面规范、全局监控接口、config.yaml监控参数、十级会员权限控制
# 功能：悬浮置顶迷你面板，展示硬件、Token、生成进度，权限动态跟随会员等级切换
from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFrame)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QFont, QColor
import json
import asyncio
from src.config.config_loader import load_global_config
from src.core.progress_monitor import get_hardware_status, get_token_flow, get_generate_progress
from src.account.member_ctrl import get_current_member_level

# 全局配置单例
GLOBAL_CFG = load_global_config()
# 监控刷新间隔读取配置文件
AI_REFRESH_SEC = GLOBAL_CFG["monitor"]["ai_monitor_refresh_sec"]
HW_REFRESH_SEC = GLOBAL_CFG["monitor"]["hardware_monitor_refresh_sec"]


class MiniMonitorWindow(QWidget):
    """
    悬浮迷你监控小窗口
    1. 全局置顶、无边框、可拖拽移动
    2. 权限动态读取当前会员等级，自动隐藏无权限监控模块
    3. 双定时器分离AI进度/硬件监控，严格匹配config.yaml刷新频率
    4. 硬件超标自动标红告警（CPU/内存/GPU阈值读取配置）
    5. 一键关闭/收起按钮，常驻后台不阻塞主程序
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        # 窗口基础属性初始化
        self._init_window_basic()
        # 初始化UI布局组件
        self._init_ui_layout()
        # 初始化刷新定时器（双任务独立调度，文档强制规范）
        self._init_monitor_timer()
        # 加载当前会员权限，动态控制模块显隐
        self._refresh_member_permission()

    def _init_window_basic(self):
        """初始化窗口基础样式：无边框、置顶、固定大小、拖拽标记"""
        # 无边框窗口
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # 固定窗口尺寸，适配悬浮迷你面板
        self.setFixedSize(260, 320)
        # 背景底色
        self.setStyleSheet("background-color: rgba(22,22,26,0.92); border-radius:8px;")
        # 拖拽坐标缓存
        self._drag_pos = None

    def _init_ui_layout(self):
        """构建页面分层布局：标题栏、硬件监控区、Token流量区、生成进度区、关闭按钮"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 10, 12, 10)
        main_layout.setSpacing(8)

        # 1. 顶部标题+关闭按钮行
        title_layout = QHBoxLayout()
        self.title_label = QLabel("羽笔·迷你监控面板")
        self.title_label.setFont(QFont("Microsoft YaHei", 10, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color:#f0f0f0;")
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(22, 22)
        self.close_btn.setStyleSheet("color:#fff;background:#c42e2e;border-radius:4px;")
        self.close_btn.clicked.connect(self.hide)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.close_btn)
        main_layout.addLayout(title_layout)

        # 分割线
        split_line = QFrame()
        split_line.setFrameShape(QFrame.Shape.HLine)
        split_line.setStyleSheet("color:#444444;")
        main_layout.addWidget(split_line)

        # 2. 硬件监控模块（CPU/内存/GPU）
        self.hw_widget = QWidget()
        hw_layout = QVBoxLayout(self.hw_widget)
        hw_layout.setSpacing(4)
        self.label_cpu = QLabel("CPU: 0%")
        self.label_mem = QLabel("内存: 0MB")
        self.label_gpu = QLabel("GPU: 0% | 显存: 0MB")
        for lab in [self.label_cpu, self.label_mem, self.label_gpu]:
            lab.setStyleSheet("color:#e0e0e0;font-size:9pt;")
            hw_layout.addWidget(lab)
        main_layout.addWidget(self.hw_widget)

        # 3. Token流量监控模块
        self.token_widget = QWidget()
        token_layout = QVBoxLayout(self.token_widget)
        token_layout.setSpacing(4)
        self.label_token_up = QLabel("上行Token: 0")
        self.label_token_down = QLabel("下行Token: 0")
        self.label_token_speed = QLabel("瞬时速率: 0 token/s")
        for lab in [self.label_token_up, self.label_token_down, self.label_token_speed]:
            lab.setStyleSheet("color:#e0e0e0;font-size:9pt;")
            token_layout.addWidget(lab)
        main_layout.addWidget(self.token_widget)

        # 4. 生成进度模块
        self.progress_widget = QWidget()
        progress_layout = QVBoxLayout(self.progress_widget)
        progress_layout.setSpacing(4)
        self.label_task_status = QLabel("任务状态: 空闲")
        self.label_gen_count = QLabel("已生成小节: 0")
        self.label_estimate = QLabel("预估剩余: --")
        for lab in [self.label_task_status, self.label_gen_count, self.label_estimate]:
            lab.setStyleSheet("color:#e0e0e0;font-size:9pt;")
            progress_layout.addWidget(lab)
        main_layout.addWidget(self.progress_widget)

        self.setLayout(main_layout)

    def _init_monitor_timer(self):
        """双定时器独立调度，遵循文档双调度独立规则"""
        # AI/Token进度定时器
        self.timer_ai = QTimer()
        self.timer_ai.setInterval(AI_REFRESH_SEC * 1000)
        self.timer_ai.timeout.connect(self.refresh_ai_token_data)
        self.timer_ai.start()

        # 硬件监控定时器
        self.timer_hw = QTimer()
        self.timer_hw.setInterval(HW_REFRESH_SEC * 1000)
        self.timer_hw.timeout.connect(self.refresh_hardware_data)
        self.timer_hw.start()

    def _refresh_member_permission(self):
        """读取当前会员等级，根据member_config.json权限动态隐藏面板模块"""
        level_info = get_current_member_level()
        level = level_info["level"]
        token_perm = level_info["monitor_token_detail"]
        ai_perm = level_info["monitor_ai_progress"]
        hw_perm = level_info["monitor_full_data"]

        # 硬件面板权限控制
        self.hw_widget.setVisible(hw_perm)
        # Token面板权限控制
        self.token_widget.setVisible(token_perm)
        # AI进度面板权限控制
        self.progress_widget.setVisible(ai_perm)

    @pyqtSlot()
    def refresh_hardware_data(self):
        """定时刷新硬件资源数据，超标标红告警，阈值读取config.yaml"""
        hw_data = get_hardware_status()
        cfg = GLOBAL_CFG["monitor"]
        cpu_warn = cfg["cpu_warn_threshold"]
        mem_warn = cfg["mem_warn_threshold"]
        gpu_warn = cfg["gpu_warn_threshold"]

        # CPU渲染
        cpu_val = hw_data["cpu_usage"]
        cpu_color = "#ff5555" if cpu_val >= cpu_warn else "#e0e0e0"
        self.label_cpu.setStyleSheet(f"color:{cpu_color};font-size:9pt;")
        self.label_cpu.setText(f"CPU: {cpu_val}%")

        # 内存渲染
        mem_val = hw_data["mem_usage"]
        mem_total = hw_data["mem_total_mb"]
        mem_color = "#ff5555" if mem_val >= mem_warn else "#e0e0e0"
        self.label_mem.setStyleSheet(f"color:{mem_color};font-size:9pt;")
        self.label_mem.setText(f"内存: {mem_val}% / {mem_total}MB")

        # GPU渲染（无N卡自动隐藏GPU行，文档硬件适配规范）
        if hw_data["gpu_enable"]:
            gpu_load = hw_data["gpu_load"]
            gpu_vram = hw_data["gpu_vram_mb"]
            gpu_color = "#ff5555" if gpu_load >= gpu_warn else "#e0e0e0"
            self.label_gpu.setStyleSheet(f"color:{gpu_color};font-size:9pt;")
            self.label_gpu.setText(f"GPU: {gpu_load}% | 显存: {gpu_vram}MB")
            self.label_gpu.setVisible(True)
        else:
            self.label_gpu.setVisible(False)

    @pyqtSlot()
    def refresh_ai_token_data(self):
        """定时刷新Token流量与AI生成进度数据"""
        token_data = get_token_flow()
        progress_data = get_generate_progress()

        # Token数据更新
        self.label_token_up.setText(f"上行Token: {token_data['prompt_total']}")
        self.label_token_down.setText(f"下行Token: {token_data['gen_total']}")
        self.label_token_speed.setText(f"瞬时速率: {token_data['speed']} token/s")

        # 生成进度更新
        task_state = progress_data["task_status"]
        done_sec = progress_data["finished_section"]
        remain_time = progress_data["estimate_remain"]
        self.label_task_status.setText(f"任务状态: {task_state}")
        self.label_gen_count.setText(f"已生成小节: {done_sec}")
        self.label_estimate.setText(f"预估剩余: {remain_time}")

    # 窗口拖拽实现
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_pos:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

    # 窗口显示时重新刷新权限，切换账号实时生效
    def showEvent(self, event):
        super().showEvent(event)
        self._refresh_member_permission()
