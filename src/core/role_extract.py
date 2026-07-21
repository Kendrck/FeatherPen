# -*- coding: utf-8 -*-
"""
自动配角识别与角色卡生成模块
文件路径：core/role_extract.py
生成标准化角色卡写入role_list.json，防止小说吃书人设崩坏
"""
import json
from core.llm_api import llm_client

class RoleExtractor:
    def extract_new_role(self, chapter_content: str, exist_role_name_list: list) -> list:
        """
        从章节正文提取未存档的新角色名称
        :param chapter_content: 刚生成完成的章节正文
        :param exist_role_name_list: 已存档角色名列表
        :return: 全新配角名称列表
        """
        system_prompt = "你是小说人物提取助手，仅输出章节内出现的全新人物姓名，以逗号分隔，无多余文字"
        user_prompt = f"现有角色：{','.join(exist_role_name_list)}\n章节正文：{chapter_content}\n找出本章出现、不在现有角色内的所有人物名字"
        raw_text = llm_client.generate_text(user_prompt, system_prompt)
        # 分割姓名，去重清洗
        name_list = [n.strip() for n in raw_text.split(",") if n.strip()]
        new_names = list(set(name_list) - set(exist_role_name_list))
        return new_names

    def build_role_card(self, role_name: str, chapter_content: str) -> dict:
        """
        根据角色名+章节剧情生成标准化角色卡
        :param role_name: 新角色姓名
        :param chapter_content: 对应章节剧情
        :return: 标准角色字典（姓名、身份、性格、人际关系、背景）
        """
        system_prompt = "你是小说人设塑造专家，输出标准JSON，字段：name,identity,personality,relation,background，无多余内容"
        user_prompt = f"角色名：{role_name}\n出场剧情：{chapter_content}\n生成完整角色档案JSON"
        json_str = llm_client.generate_text(user_prompt, system_prompt)
        # 解析AI返回的角色JSON
        role_card = json.loads(json_str)
        return role_card

# 全局角色提取实例
role_extractor = RoleExtractor()
