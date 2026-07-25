from pathlib import Path

p = Path("docs/STRUCTURE.md")
text = p.read_text(encoding="utf-8")
marker = "# FeatherPen/docs/STRUCTURE.md\n# FeatherPen V1.0.0 STRUCTURE文件结构树标准仓库完整目录架构文档\n# 排序规则：文件夹优先按字母升序，同层级文件按英文字母升序排列\n# 注释规范：# 后为文件/文件夹标准化业务说明，强制约束加粗标注\n# 文档基准优先级：本目录规范 > 全平台兼容性规范 > 初代开发规范文档\n# 架构变更说明：永久移除ui/PyQt6、electron目录，统一采用web/原生HTML + PyWebView桌面壳架构\n# GB/T 8567-2006 软件文档编制规范配套归档文件\n# 同步规则：所有新增/修改/删除文件，必须完整录入本文档；代码改动同步更新开发文档，文件与文档全程可追溯\n\nFeatherPen/ # 项目根一级目录\n"
first = text.find(marker)
second = text.find(marker, first + len(marker))
if second != -1:
    text = text[:second]
p.write_text(text, encoding="utf-8")
print("deduped")
