# -*- coding: utf-8 -*-
"""
角色自动提取与归档模块 V1.0.0
功能：从章节正文解析角色信息、自动去重、持久化归档、自动积分扣费
"""
import json
import os
from src.account.point_system import point_deduct

def extract_and_archive_role(book_path: str, chapter_content: str):
    """
    解析章节内容并归档角色数据
    :param book_path: 当前小说工程根路径
    :param chapter_content: 待解析章节正文内容
    :return: 归档完成后的全量角色列表
    """
    # 执行角色整理扣费（固定1积分）
    point_deduct("sort_role")
    # 角色归档文件路径
    role_file = f"{book_path}/role_list.json"
    # 读取已有角色数据
    old_roles = []
    if os.path.exists(role_file):
        with open(role_file, "r", encoding="utf-8") as f:
            old_roles = json.load(f)
    # 新增角色解析、去重逻辑预留位
    new_roles = []
    final_roles = old_roles + new_roles
    # 写入最新角色归档数据
    with open(role_file, "w", encoding="utf-8") as f:
        json.dump(final_roles, f, ensure_ascii=False, indent=2)
    return final_roles
