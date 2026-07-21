# 文件路径: lib/core.py

# 导入相对路径下的语言包模块
from .lang import get_text

class FeatherPen:
    """
    FeatherPen 核心类
    负责处理主要的业务逻辑，并支持多语言输出
    """
    def __init__(self, lang_code="zh_CN"):
        """
        初始化 FeatherPen
        :param lang_code: 语言代码，默认为简体中文
        """
        self.lang_code = lang_code
        print(get_text("init_success", self.lang_code))

    def write(self, content):
        """
        执行书写操作
        :param content: 需要书写的内容
        """
        # 从语言包中获取提示信息并格式化
        message = get_text("writing_content", self.lang_code).format(content=content)
        print(message)
        return True
