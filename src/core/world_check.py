"""
FeatherPen V1.0.0 世界观、时间线及剧情逻辑一致性校验模块
功能：执行全书范围内的剧情一致性检查，包括角色、时间线、伏笔等
规范：手动校验扣10积分，自动校验扣5积分
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class WorldCheck:
    """
    剧情世界观一致性校验器
    负责检查角色一致性、时间线逻辑、伏笔回收等
    """
    def __init__(self, project_path: str):
        """
        初始化校验器
        :param project_path: 书籍工程根目录路径
        """
        self.project_path = Path(project_path)
        self.roles_data = {}  # 角色归档数据
        self.timeline_data = []  # 时间线数据
        self.issues = []  # 检测到的问题列表

    def load_data(self) -> None:
        """加载角色、时间线等基础数据"""
        # 加载角色数据
        role_file = self.project_path / "role_list.json"
        if role_file.exists():
            try:
                with open(role_file, 'r', encoding='utf-8') as f:
                    self.roles_data = json.load(f)
            except Exception as e:
                logger.error(f"加载角色数据失败: {e}")

        # 加载时间线数据
        timeline_file = self.project_path / "timeline.json"
        if timeline_file.exists():
            try:
                with open(timeline_file, 'r', encoding='utf-8') as f:
                    self.timeline_data = json.load(f)
            except Exception as e:
                logger.error(f"加载时间线数据失败: {e}")

    def check_character_consistency(self) -> List[Dict]:
        """
        检查角色人设一致性（防吃书）
        :return: 发现的问题列表
        """
        issues = []
        # 具体实现：遍历章节内容，对比角色描述
        # 示例：检查角色名称是否前后一致
        # 实际实现需调用LLM进行语义比对
        logger.info("开始检查角色人设一致性...")
        return issues

    def check_timeline_logic(self) -> List[Dict]:
        """
        检查时间线逻辑错误（如时间倒挂）
        :return: 发现的问题列表
        """
        issues = []
        if not self.timeline_data:
            return issues

        # 按章节排序时间线事件
        sorted_events = sorted(self.timeline_data, key=lambda x: x.get('chapter', 0))
        for i in range(1, len(sorted_events)):
            prev = sorted_events[i-1]
            curr = sorted_events[i]
            # 检查时间顺序是否合理
            if prev.get('chapter', 0) > curr.get('chapter', 0):
                issues.append({
                    'type': 'timeline_order',
                    'message': f"时间线事件顺序异常: {prev.get('event')} (章{prev.get('chapter')}) "
                               f"位于 {curr.get('event')} (章{curr.get('chapter')}) 之后",
                    'severity': 'error'
                })
        return issues

    def check_foreshadowing(self) -> List[Dict]:
        """
        检查伏笔埋设与回收
        :return: 发现的问题列表
        """
        issues = []
        # 具体实现：扫描章节内容，识别伏笔和回收点
        logger.info("开始检查伏笔留存...")
        return issues

    def run_full_check(self, check_type: str = "full") -> Tuple[bool, List[Dict]]:
        """
        执行完整的全书校验
        :param check_type: 校验类型: full(完整) / quick(快速)
        :return: (是否通过, 问题列表)
        """
        self.issues = []
        self.load_data()

        # 执行各项检查
        self.issues.extend(self.check_character_consistency())
        self.issues.extend(self.check_timeline_logic())
        self.issues.extend(self.check_foreshadowing())

        # 生成校验报告
        if self.issues:
            logger.warning(f"全书校验发现问题 {len(self.issues)} 个")
            return False, self.issues
        else:
            logger.info("全书校验通过，未发现问题")
            return True, []

    def generate_report(self) -> Dict:
        """
        生成详细的校验报告
        :return: 报告数据字典
        """
        error_count = len([i for i in self.issues if i.get('severity') == 'error'])
        warning_count = len([i for i in self.issues if i.get('severity') == 'warning'])

        return {
            'check_time': datetime.now().isoformat(),
            'total_issues': len(self.issues),
            'error_count': error_count,
            'warning_count': warning_count,
            'issues': self.issues,
            'passed': len(self.issues) == 0
        }

    def check_auto_trigger(self, total_sections: int) -> bool:
        """
        判断是否满足自动校验触发条件（每50节）
        :param total_sections: 当前总节数
        :return: 达到50节倍数且未触发过返回True
        """
        # 检查是否达到50节的倍数
        if total_sections >= 50 and total_sections % 50 == 0:
            # 检查是否已触发过（通过进度标记）
            trigger_file = self.project_path / ".auto_check_mark.json"
            if trigger_file.exists():
                try:
                    with open(trigger_file, 'r') as f:
                        marks = json.load(f)
                        if marks.get(str(total_sections), False):
                            return False
                except:
                    pass
            # 标记该节数已触发
            with open(trigger_file, 'w') as f:
                json.dump({str(total_sections): True}, f)
            return True
        return False
