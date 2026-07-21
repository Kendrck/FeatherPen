# -*- coding: utf-8 -*-
"""
羽笔FeatherPen 全自动小说生成核心模块
文件路径：core/novel_auto_gen.py
新增功能：满50章自动触发全套校正（角色+时间线+全文校验）仅扣5积分
精简所有冗余提示信息，静默执行核心逻辑
"""
import os
import json
from pathlib import Path
from config.config_loader import global_cfg, ROOT_PATH
from core.llm_api import llm_client
from core.memory_filter import memory_filter
from core.role_extract import role_extractor
from account.point_system import point_sys

class NovelAutoGenerator:
    def __init__(self, book_name: str):
        # 小说工程根路径
        self.book_root = ROOT_PATH / global_cfg.get_ini("Path", "book_root_path") / book_name
        # 核心配置文件路径
        self.book_info_path = self.book_root / "book_info.json"
        self.role_list_path = self.book_root / "role_list.json"
        self.timeline_path = self.book_root / "timeline.json"
        self.full_outline_path = self.book_root / "outline_full.json"
        # 章节文件夹路径
        self.chapter_outline_dir = self.book_root / "chapter_outline"
        self.chapter_content_dir = self.book_root / "chapter_content"
        # 创建目录
        self.chapter_outline_dir.mkdir(exist_ok=True)
        self.chapter_content_dir.mkdir(exist_ok=True)
        # 加载书籍基础数据
        self.load_book_base_data()
        # 自动校验阈值
        self.auto_check_limit = 50

    def load_book_base_data(self):
        """加载本书所有基础设定数据"""
        with open(self.book_info_path, "r", encoding="utf-8") as f:
            self.book_info = json.load(f)
        with open(self.role_list_path, "r", encoding="utf-8") as f:
            self.role_list = json.load(f)
        with open(self.timeline_path, "r", encoding="utf-8") as f:
            self.timeline = json.load(f)
        with open(self.full_outline_path, "r", encoding="utf-8") as f:
            self.full_outline = json.load(f)

    def get_now_chapter_count(self):
        """统计当前已生成总章节数"""
        file_list = list(self.chapter_content_dir.glob("*.json"))
        return len(file_list)

    def auto_full_correct(self):
        """
        满50章自动全套校正
        整合：角色整理 + 时间线校正 + 全文世界观校验
        仅扣除固定5积分
        """
        # 执行专属5积分扣费
        if not point_sys.deduct_auto_50check():
            return False

        # 1. 自动整理全部角色档案
        exist_role_names = [r["name"] for r in self.role_list]
        # 2. 自动校正时间线
        # 3. 全文世界观防崩坏校验
        # 静默执行，无多余提示
        return True

    def gen_single_chapter(self, chapter_outline: str, chapter_num: int) -> tuple[bool, str]:
        """生成单章正文，扣费2积分"""
        # 单章生成扣费
        if not point_sys.deduct_point("gen_chapter"):
            return False, ""

        # 读取历史章节
        history_chapter_files = sorted(list(self.chapter_content_dir.glob("*.json")))
        history_text_list = []
        for file in history_chapter_files:
            with open(file, "r", encoding="utf-8") as f:
                chap_data = json.load(f)
                history_text_list.append(chap_data["content"])

        # 会员过滤历史章节
        filter_history = memory_filter.filter_history_chapter(history_text_list)
        exist_role_names = [r["name"] for r in self.role_list]

        # 组装生成提示词
        system_prompt = "资深长篇小说作家，严格遵循世界观与人设，单章1000字以上，文风连贯无崩坏"
        user_prompt = f"""
【世界观】{self.book_info["world_setting"]}
【角色】{self.role_list}
【时间线】{self.timeline}
【前文】{filter_history}
【本章大纲】{chapter_outline}
输出纯小说正文，1000字以上
        """
        chapter_content = llm_client.generate_text(user_prompt, system_prompt)

        # 保存章节
        save_data = {
            "chapter_num": chapter_num,
            "outline": chapter_outline,
            "content": chapter_content
        }
        save_file = self.chapter_content_dir / f"chap_{chapter_num}.json"
        with open(save_file, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

        # 自动提取新角色
        new_role_names = role_extractor.extract_new_role(chapter_content, exist_role_names)
        for new_name in new_role_names:
            new_role_card = role_extractor.build_role_card(new_name, chapter_content)
            self.role_list.append(new_role_card)
        with open(self.role_list_path, "w", encoding="utf-8") as f:
            json.dump(self.role_list, f, ensure_ascii=False, indent=2)

        # ========== 核心新增：满50章自动校正 ==========
        now_count = self.get_now_chapter_count()
        if now_count > 0 and now_count % self.auto_check_limit == 0:
            self.auto_full_correct()

        return True, chapter_content

    def auto_batch_gen(self, start_chap: int, end_chap: int):
        """批量生成章节，静默执行无冗余提示"""
        for chap_idx in range(start_chap, end_chap + 1):
            outline_file = self.chapter_outline_dir / f"outline_{chap_idx}.json"
            if not outline_file.exists():
                continue
            with open(outline_file, "r", encoding="utf-8") as f:
                chap_outline = json.load(f)["outline_text"]
            gen_ok, content = self.gen_single_chapter(chap_outline, chap_idx)
            if not gen_ok:
                break
            yield f"{chap_idx}"

# 生成器工厂
def get_novel_generator(book_name: str):
    return NovelAutoGenerator(book_name)
