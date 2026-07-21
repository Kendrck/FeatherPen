"""
FeatherPen V1.0.0 会员等级动态适配与权限校验模块
功能：管理会员等级、权限规则校验与拦截，实时响应账号状态变更
规范：严格遵循member_config.json定义的十级会员权限体系
"""
import json
import logging
from typing import Dict, Optional, Tuple
from pathlib import Path

# FeatherPen/src/account/member_ctrl.py

import time
from typing import Dict, Any

class MemberController:
    """
    会员权限与状态控制器
    处理等级判定、昵称显示及按小时扣费逻辑
    """
    
    # 管理员 UID 列表 (11111111 - 00000000)
    ADMIN_UIDS = [str(i) * 8 for i in range(1, 10)] + ["00000000"]

    @staticmethod
    def get_display_name(user_info: Dict[str, Any]) -> str:
        """
        获取前端展示昵称
        优先显示自定义昵称，无昵称则显示8位数字ID
        """
        nickname = user_info.get("ext_info", {}).get("nickname", "")
        if nickname:
            return nickname
        return user_info.get("username", "未知用户")

    @staticmethod
    def check_hourly_deduction(user_info: Dict[str, Any]) -> bool:
        """
        校验是否允许按小时扣费
        :return: True=允许扣费/放行, False=积分不足或账号异常
        """
        uid = user_info.get("username")
        ext_info = user_info.get("ext_info", {})
        
        # 1. 9级管理员或特定UID直接放行
        if ext_info.get("level") == 9 or uid in MemberController.ADMIN_UIDS:
            return True
            
        # 2. 普通用户校验积分
        points = ext_info.get("points", 0)
        if points > 0:
            # TODO: 此处可调用 YesApi 接口扣除1点积分
            return True
            
        return False


logger = logging.getLogger(__name__)

class MemberController:
    """
    会员控制器，负责加载会员配置、校验权限、管理当前会员状态
    """
    def __init__(self, config_path: str = "member_config.json"):
        """
        初始化会员控制器
        :param config_path: 会员配置文件的路径
        """
        self.config_path = Path(config_path)
        self.member_config = self._load_config()
        self.current_level = 0  # 默认离线Lv0
        self.current_uid = None

    def _load_config(self) -> Dict:
        """加载会员配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"会员配置文件未找到: {self.config_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"会员配置文件格式错误: {self.config_path}")
            raise

    def get_level_config(self, level: int) -> Optional[Dict]:
        """
        获取指定等级的完整配置
        :param level: 会员等级 (0-9)
        :return: 等级配置字典，如果等级不存在则返回None
        """
        for item in self.member_config.get('member_level', []):
            if item.get('level') == level:
                return item
        return None

    def set_current_user(self, uid: Optional[str] = None) -> None:
        """
        设置当前登录用户，自动切换会员等级
        :param uid: 用户ID，None表示离线状态
        """
        if uid is None:
            # 离线状态：固定Lv0
            self.current_level = 0
            self.current_uid = None
            logger.info("用户已离线，切换至Lv0无名")
            return

        # 登录状态：查找用户对应的等级
        for user in self.member_config.get('default_member_list', []):
            if user.get('uid') == uid:
                self.current_level = user.get('level', 1)
                self.current_uid = uid
                logger.info(f"用户 {uid} 登录，等级: Lv{self.current_level}")
                return

        # 未找到用户，默认Lv1（登录最低等级）
        self.current_level = 1
        self.current_uid = uid
        logger.warning(f"未找到用户 {uid} 的等级配置，默认Lv1初闻")

    def check_permission(self, permission_type: str) -> bool:
        """
        校验当前用户是否拥有指定权限
        :param permission_type: 权限类型，如 'world_check', 'monitor_full_data'
        :return: 拥有权限返回True，否则返回False
        """
        config = self.get_level_config(self.current_level)
        if config is None:
            return False
        return config.get(permission_type, False)

    def get_creation_limits(self) -> Tuple[int, int, int]:
        """
        获取当前等级的创作上限
        :return: (历史章节投喂上限, 大纲投喂上限, 单次批量生成上限)
        """
        config = self.get_level_config(self.current_level)
        if config is None:
            return (0, 0, 0)
        return (
            config.get('max_send_chapter', 0),
            config.get('max_send_outline', 0),
            config.get('max_output_chapter', 0)
        )

    def get_daily_point_limit(self) -> int:
        """
        获取当前等级的日积分消耗上限
        :return: 日积分上限，Lv0为10，其他等级为-1表示无限制
        """
        if self.current_level == 0:
            return 10
        return -1  # -1表示无限制

    def get_level_name(self) -> str:
        """获取当前等级的显示名称"""
        config = self.get_level_config(self.current_level)
        if config:
            return config.get('level_name', f'Lv{self.current_level}')
        return f'Lv{self.current_level}'

    def get_current_level(self) -> int:
        """获取当前会员等级"""
        return self.current_level
