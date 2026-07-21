# -*- coding: utf-8 -*-
"""
上下文智能筛选模块 V1.0.0
功能：根据用户会员等级，自动过滤历史章节、大纲投喂数量
严格匹配各等级创作上限规则，防止上下文溢出
"""
from src.account.member_ctrl import get_user_level_info

def filter_history_context(user_level: int, all_chapter: list, all_outline: list):
    """
    筛选当前用户可使用的历史上下文数据
    :param user_level: 用户会员等级
    :param all_chapter: 全部历史章节列表
    :param all_outline: 全部历史大纲列表
    :return: 筛选后的可用章节、大纲数据
    """
    level_info = get_user_level_info(user_level)
    # 按等级上限截取最新的历史数据
    filter_chapter = all_chapter[-level_info["max_send_chapter"]:] if all_chapter else []
    filter_outline = all_outline[-level_info["max_send_outline"]:] if all_outline else []
    return filter_chapter, filter_outline
