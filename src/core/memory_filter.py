# -*- coding: utf-8 -*-
"""上下文素材智能过滤模块。"""

from __future__ import annotations

from typing import Any, Dict


class MemoryFilter:
    def __init__(self) -> None:
        self.user_limit: Dict[str, Any] = {"max_send_chapter": 5, "max_send_outline": 10}

    def filter_history_chapter(self, all_chapter_list: list) -> list:
        """
        过滤历史章节，只保留会员允许的最新章节
        :param all_chapter_list: 全书所有章节正文列表（按顺序）
        :return: 截取后的最新章节列表
        """
        max_send = self.user_limit["max_send_chapter"]
        if len(all_chapter_list) <= max_send:
            return all_chapter_list
        # 截取末尾N章最新内容，减少上下文长度
        return all_chapter_list[-max_send:]

    def filter_outline(self, all_outline_list: list) -> list:
        """过滤章节大纲，控制投喂大纲数量上限"""
        max_outline = self.user_limit["max_send_outline"]
        if len(all_outline_list) <= max_outline:
            return all_outline_list
        return all_outline_list[-max_outline:]

    def filter_unused_role(self, all_role_list: list, current_chapter_char_names: list) -> list:
        """
        过滤不出场角色，仅保留本章出场角色投喂模型，节省token
        :param all_role_list: 全书全部角色卡
        :param current_chapter_char_names: 当前章节出现的角色名列表
        :return: 仅出场角色的角色卡列表
        """
        res = []
        for role in all_role_list:
            if role["name"] in current_chapter_char_names:
                res.append(role)
        return res

# 全局过滤实例
memory_filter = MemoryFilter()
