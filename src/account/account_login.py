# -*- coding: utf-8 -*-
"""
账号登录状态校验模块 V1.0.0
核心规则：
1. 无用户配置文件默认离线Lv0
2. 登录成功最低等级Lv1
3. 退出/注销自动回退Lv0离线状态
功能：登录状态检测、账号注销、权限状态重置
"""
import json
import os
from src.database.db_sqlite import db_query


# FeatherPen/src/account/account_login.py

import hashlib
import requests
from typing import Optional, Dict, Any
from src.config.config_loader import get_config

class AccountLogin:
    """
    账号登录与派发核心控制器
    负责与 YesApi 云端通信，处理账号的登录、状态校验及初始派发
    """
    def __init__(self):
        self.api_url = "https://api.yesapi.cn/"
        self.app_key = get_config("YESAPI_APP_KEY")
        self.app_secret = get_config("YESAPI_APP_SECRET")

    def _generate_sign(self, params: Dict[str, Any]) -> str:
        """
        生成 YesApi 请求签名 (安全防篡改)
        """
        # 1. 按 key 字典序排序
        sorted_keys = sorted(params.keys())
        # 2. 拼接参数
        str_to_sign = ""
        for key in sorted_keys:
            str_to_sign += f"{key}{params[key]}"
        # 3. 尾部追加 AppSecret 并做 MD5 加密
        str_to_sign += self.app_secret
        return hashlib.md5(str_to_sign.encode('utf-8')).hexdigest()

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        用户登录接口
        :param username: 8位纯数字账号
        :param password: 用户密码
        :return: 包含用户信息、等级、积分的字典
        """
        params = {
            "s": "App.User.Login",
            "app_key": self.app_key,
            "username": username,
            "password": hashlib.md5(password.encode('utf-8')).hexdigest()
        }
        params["sign"] = self._generate_sign(params)
        
        response = requests.get(self.api_url, params=params).json()
        if response.get("ret") == 200:
            return response["data"]["info"]
        raise Exception(f"登录失败: {response.get('msg', '未知错误')}")

    def get_pending_account(self) -> Optional[str]:
        """
        【发牌官逻辑】从云端获取一个待派发的账号
        """
        params = {
            "s": "App.Table.List",
            "app_key": self.app_key,
            "model_name": "yesapi_member",
            "where": '[["account_status","=","pending"]]',
            "limit": 1
        }
        params["sign"] = self._generate_sign(params)
        response = requests.get(self.api_url, params=params).json()
        
        if response.get("ret") == 200 and response["data"].get("list"):
            return response["data"]["list"][0]["username"]
        return None

def check_login_status():
    """
    检测当前用户登录状态与会员等级
    :return: is_login(是否登录:bool), user_level(会员等级:int)
    """
    user_config_path = "Book/User/user_setting.json"
    # 无用户配置文件判定为离线状态
    if not os.path.exists(user_config_path):
        return False, 0
    # 读取用户本地配置
    with open(user_config_path, "r", encoding="utf-8") as f:
        user_data = json.load(f)
    is_login = user_data.get("is_login", False)
    # 登录状态默认最低Lv1，离线固定Lv0
    user_level = user_data.get("level", 1) if is_login else 0
    return is_login, user_level

def user_logout():
    """
    用户注销退出登录
    执行逻辑：重置登录状态、会员等级，自动切换为离线Lv0
    """
    user_config_path = "Book/User/user_setting.json"
    if not os.path.exists(user_config_path):
        return
    # 读取原有用户数据
    with open(user_config_path, "r", encoding="utf-8") as f:
        user_data = json.load(f)
    # 重置为离线状态
    user_data["is_login"] = False
    user_data["level"] = 0
    # 写入更新后配置
    with open(user_config_path, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)
