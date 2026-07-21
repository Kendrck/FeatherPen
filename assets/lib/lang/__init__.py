# 文件路径: lib/lang/__init__.py

# 导入具体的语言字典
from .zh_CN import TEXTS as ZH_CN_TEXTS
from .en_US import TEXTS as EN_US_TEXTS

# 语言映射字典，方便后续扩展新语言
LANGUAGES = {
    "zh_CN": ZH_CN_TEXTS,
    "en_US": EN_US_TEXTS
}

def get_text(key, lang_code="zh_CN"):
    """
    获取指定语言的文本
    :param key: 文本的键名
    :param lang_code: 语言代码
    :return: 对应的翻译文本
    """
    # 如果找不到对应语言，默认回退到英文
    lang_dict = LANGUAGES.get(lang_code, EN_US_TEXTS)
    return lang_dict.get(key, key)
