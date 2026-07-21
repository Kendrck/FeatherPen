"""
FeatherPen V1.0.0 全自动长篇小说生成调度模块
功能：统筹全书卷/章/节大纲，按「节」为最小单元批量生成正文
规范：严格遵循三级创作层级，支持断点续跑和进度持久化
"""
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class NovelAutoGenerator:
    """
    全自动小说生成调度器
    负责管理生成任务、调用LLM引擎、维护进度状态
    """
    def __init__(self, project_path: str, llm_engine):
        """
        初始化生成器
        :param project_path: 书籍工程根目录路径
        :param llm_engine: LLM引擎实例，用于调用生成接口
        """
        self.project_path = Path(project_path)
        self.llm_engine = llm_engine
        self.outline_data = None  # 全书大纲数据
        self.progress_data = {}   # 当前生成进度
        self.current_section = None  # 当前生成的节信息
        self.is_running = False

    def load_outline(self, outline_path: str = "outline_full.json") -> bool:
        """
        加载全书卷章大纲
        :param outline_path: 大纲文件相对路径
        :return: 加载成功返回True
        """
        full_path = self.project_path / outline_path
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                self.outline_data = json.load(f)
            logger.info(f"成功加载大纲: {full_path}")
            return True
        except FileNotFoundError:
            logger.error(f"大纲文件未找到: {full_path}")
            return False
        except json.JSONDecodeError:
            logger.error(f"大纲文件格式错误: {full_path}")
            return False

    def calculate_total_sections(self) -> int:
        """
        计算全书总节数
        :return: 全书总节数
        """
        if not self.outline_data:
            return 0
        total = 0
        for volume in self.outline_data.get('volumes', []):
            for chapter in volume.get('chapters', []):
                total += len(chapter.get('sections', []))
        return total

    def get_next_section(self) -> Optional[Dict]:
        """
        获取下一个待生成的节（基于进度）
        :return: 节信息字典，若无待生成节则返回None
        """
        if not self.outline_data:
            return None

        # 遍历卷、章、节，查找未生成的节
        for volume in self.outline_data.get('volumes', []):
            vol_idx = volume.get('index', 0)
            for chapter in volume.get('chapters', []):
                chap_idx = chapter.get('index', 0)
                for section in chapter.get('sections', []):
                    sec_idx = section.get('index', 0)
                    # 检查该节是否已生成
                    if not self._is_section_generated(vol_idx, chap_idx, sec_idx):
                        return {
                            'volume': volume,
                            'volume_index': vol_idx,
                            'chapter': chapter,
                            'chapter_index': chap_idx,
                            'section': section,
                            'section_index': sec_idx,
                            'prompt': section.get('prompt', '')
                        }
        return None

    def _is_section_generated(self, vol_idx: int, chap_idx: int, sec_idx: int) -> bool:
        """
        检查指定节是否已生成
        :param vol_idx: 卷索引
        :param chap_idx: 章索引
        :param sec_idx: 节索引
        :return: 已生成返回True
        """
        progress_key = f"{vol_idx}_{chap_idx}_{sec_idx}"
        return self.progress_data.get(progress_key, {}).get('generated', False)

    async def generate_next_section(self) -> Tuple[bool, str]:
        """
        异步生成下一节正文
        :return: (是否成功, 生成的正文或错误信息)
        """
        # 1. 获取待生成节
        section_info = self.get_next_section()
        if not section_info:
            logger.info("全书所有节已生成完毕")
            return True, "全书所有节已生成完毕"

        self.current_section = section_info
        self.is_running = True

        try:
            # 2. 构造生成提示词（包含上下文）
            prompt = self._build_prompt(section_info)
            context_id = f"gen_{int(time.time())}"

            # 3. 调用LLM引擎生成
            full_text = ""
            async for chunk in self.llm_engine.generate_stream(prompt, context_id):
                full_text += chunk

            # 4. 保存生成的正文
            if full_text.strip():
                await self._save_section_content(section_info, full_text)
                self._mark_section_generated(section_info)
                logger.info(f"成功生成第{section_info['volume_index']}卷"
                            f"第{section_info['chapter_index']}章"
                            f"第{section_info['section_index']}节")
                return True, full_text
            else:
                logger.warning("生成内容为空")
                return False, "生成内容为空"

        except Exception as e:
            logger.error(f"生成节内容失败: {e}")
            return False, str(e)
        finally:
            self.is_running = False

    def _build_prompt(self, section_info: Dict) -> str:
        """
        根据节信息构建生成提示词
        :param section_info: 节信息字典
        :return: 完整的提示词字符串
        """
        # 实际实现中需包含历史上下文、角色信息等
        prompt = f"""
请根据以下大纲撰写小说正文：

【卷大纲】：{section_info['volume'].get('outline', '')}
【章大纲】：{section_info['chapter'].get('outline', '')}
【节细纲】：{section_info['section'].get('outline', '')}
【提示词】：{section_info.get('prompt', '')}

请以流畅的小说语言进行创作，约1000字。
"""
        return prompt

    async def _save_section_content(self, section_info: Dict, content: str) -> None:
        """
        保存生成的节正文到文件
        :param section_info: 节信息
        :param content: 生成的正文
        """
        vol_idx = section_info['volume_index']
        chap_idx = section_info['chapter_index']
        sec_idx = section_info['section_index']
        # 构建存储路径: Book/书名/chapter_content/卷_章_节.txt
        file_name = f"V{vol_idx:02d}_C{chap_idx:03d}_S{sec_idx:03d}.txt"
        save_dir = self.project_path / "chapter_content"
        save_dir.mkdir(parents=True, exist_ok=True)
        file_path = save_dir / file_name

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _mark_section_generated(self, section_info: Dict) -> None:
        """
        标记节为已生成，更新进度
        :param section_info: 节信息
        """
        key = f"{section_info['volume_index']}_{section_info['chapter_index']}_{section_info['section_index']}"
        self.progress_data[key] = {
            'generated': True,
            'timestamp': datetime.now().isoformat(),
            'file': f"V{section_info['volume_index']:02d}_C{section_info['chapter_index']:03d}_S{section_info['section_index']:03d}.txt"
        }
        self._save_progress()

    def _save_progress(self) -> None:
        """保存当前进度快照"""
        progress_file = self.project_path / ".progress.json"
        try:
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存进度文件失败: {e}")

    def load_progress(self) -> None:
        """加载进度快照，用于断点续跑"""
        progress_file = self.project_path / ".progress.json"
        if progress_file.exists():
            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    self.progress_data = json.load(f)
                logger.info(f"加载进度快照成功，已生成 {len(self.progress_data)} 节")
            except Exception as e:
                logger.error(f"加载进度文件失败: {e}")
                self.progress_data = {}
        else:
            logger.info("无历史进度，开始全新生成")
            self.progress_data = {}

    def get_generation_status(self) -> Dict:
        """
        获取当前生成进度状态
        :return: 进度统计信息字典
        """
        total = self.calculate_total_sections()
        completed = len([k for k, v in self.progress_data.items() if v.get('generated')])
        return {
            'total_sections': total,
            'completed_sections': completed,
            'remaining_sections': max(0, total - completed),
            'progress_percent': (completed / total * 100) if total > 0 else 0
        }
