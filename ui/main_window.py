"""
FeatherPen V1.0.0 主窗口UI模块
功能：初始化主窗口、管理页面路由、调度全局事件
规范：基于PyQt6，支持多页面切换和响应式布局
"""
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction

class MainWindow(QMainWindow):
    """
    羽笔主窗口类
    负责全局UI布局、页面切换和核心事件调度
    """
    # 定义全局信号
    login_status_changed = pyqtSignal(bool)  # 登录状态变更信号
    model_ready_changed = pyqtSignal(bool)   # 模型就绪状态信号

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.setWindowTitle("FeatherPen 羽笔 V1.0.0")
        self.setMinimumSize(1200, 800)
        self.current_user = None  # 当前用户信息

        # 初始化UI组件
        self._init_ui()
        self._init_menu_bar()
        self._connect_signals()

        # 应用初始样式
        self._apply_style()

    def _init_ui(self) -> None:
        """初始化界面布局"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. 顶部导航栏
        self.nav_bar = self._create_nav_bar()
        main_layout.addWidget(self.nav_bar)

        # 2. 内容堆叠区域（用于页面切换）
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

        # 3. 初始化各个页面
        self._init_pages()

        # 默认显示工作台页面
        self.content_stack.setCurrentIndex(1)

    def _create_nav_bar(self) -> QWidget:
        """创建顶部导航栏"""
        nav_widget = QWidget()
        nav_widget.setFixedHeight(50)
        nav_widget.setObjectName("navBar")
        layout = QHBoxLayout(nav_widget)
        layout.setContentsMargins(20, 0, 20, 0)

        # Logo和标题
        title_label = QLabel("🪶 羽笔")
        title_label.setObjectName("navTitle")
        layout.addWidget(title_label)

        # 导航按钮
        self.nav_buttons = {}
        nav_items = [
            ("工作台", "workbench"),
            ("创作", "novel"),
            ("会员", "member"),
            ("模型设置", "settings"),
            ("监控", "monitor")
        ]
        for text, name in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=name: self.switch_page(n))
            layout.addWidget(btn)
            self.nav_buttons[name] = btn

        layout.addStretch()

        # 用户状态显示
        self.user_status_label = QLabel("未登录 | Lv0 无名")
        self.user_status_label.setObjectName("userStatus")
        layout.addWidget(self.user_status_label)

        return nav_widget

    def _init_pages(self) -> None:
        """初始化所有页面"""
        from ui.login_ui import LoginUI
        from ui.novel_workbench import NovelWorkbench
        from ui.member_panel import MemberPanel
        from ui.model_setting_ui import ModelSettingUI
        from ui.monitor_dashboard import MonitorDashboard

        # 页面列表 (索引, 名称, 实例)
        pages = [
            (0, "login", LoginUI()),
            (1, "workbench", NovelWorkbench()),
            (2, "novel", NovelWorkbench()),  # 实际可复用或单独实现
            (3, "member", MemberPanel()),
            (4, "settings", ModelSettingUI()),
            (5, "monitor", MonitorDashboard())
        ]
        self.page_map = {}
        for idx, name, widget in pages:
            self.content_stack.addWidget(widget)
            self.page_map[name] = idx

    def _init_menu_bar(self) -> None:
        """初始化菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        new_action = QAction("新建工程(&N)", self)
        new_action.triggered.connect(self._on_new_project)
        file_menu.addAction(new_action)

        open_action = QAction("打开工程(&O)", self)
        open_action.triggered.connect(self._on_open_project)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QAction("退出(&X)", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _connect_signals(self) -> None:
        """连接信号与槽"""
        # 登录状态变更时更新UI
        self.login_status_changed.connect(self._update_user_status)

    def _apply_style(self) -> None:
        """应用全局样式表"""
        style = """
            QMainWindow {
                background-color: #f5f5f5;
            }
            #navBar {
                background-color: #2c3e50;
                color: white;
            }
            #navTitle {
                font-size: 18px;
                font-weight: bold;
                color: white;
            }
            #navBtn {
                background-color: transparent;
                color: #bdc3c7;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
            }
            #navBtn:hover {
                color: white;
                background-color: #34495e;
            }
            #navBtn:checked {
                color: white;
                border-bottom: 2px solid #3498db;
            }
            #userStatus {
                color: #ecf0f1;
                font-size: 12px;
            }
        """
        self.setStyleSheet(style)

    def switch_page(self, page_name: str) -> None:
        """
        切换当前显示的页面
        :param page_name: 页面名称 (workbench/member/settings/monitor)
        """
        if page_name in self.page_map:
            self.content_stack.setCurrentIndex(self.page_map[page_name])
            # 更新导航按钮状态
            for name, btn in self.nav_buttons.items():
                btn.setChecked(name == page_name)

    def _update_user_status(self, is_logged_in: bool) -> None:
        """更新用户状态显示"""
        if is_logged_in and self.current_user:
            level = self.current_user.get('level', 1)
            level_name = self.current_user.get('level_name', '初闻')
            self.user_status_label.setText(f"已登录 | Lv{level} {level_name}")
        else:
            self.user_status_label.setText("未登录 | Lv0 无名")

    def _on_new_project(self) -> None:
        """新建工程"""
        # TODO: 实现新建工程对话框
        print("新建工程")

    def _on_open_project(self) -> None:
        """打开工程"""
        # TODO: 实现打开工程对话框
        print("打开工程")

    def _on_about(self) -> None:
        """显示关于对话框"""
        # TODO: 实现关于对话框
        print("FeatherPen 羽笔 V1.0.0")

    def closeEvent(self, event) -> None:
        """窗口关闭事件处理"""
        # 执行清理工作
        event.accept()