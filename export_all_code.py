import os

# ========== 配置区 ==========
ROOT_DIR = r"D:\FeatherPen"
OUTPUT_FILE = r"D:\FeatherPen\daima.txt"
# 需要导出的文本后缀
INCLUDE_EXT = {".py", ".yaml", ".yml", ".json", ".md", ".ini", ".txt", ".toml", ".bat", ".env.example"}
# 需要跳过的目录（虚拟环境、编译产物、缓存）
SKIP_DIRS = {"venv", ".venv", "dist", "build", "__pycache__", ".git", ".vscode", "runtime"}
# ===========================

def export_project_code():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        out_f.write("===== FeatherPen 项目完整代码导出 =====\n\n")

        for root, dirs, files in os.walk(ROOT_DIR):
            # 过滤跳过目录
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

            for filename in files:
                ext = os.path.splitext(filename)[1].lower()
                if ext not in INCLUDE_EXT:
                    continue

                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, ROOT_DIR)

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    content = f"【读取失败】{e}"

                # 写入分割标记
                out_f.write(f"===============================\n【文件路径】{rel_path}\n===============================\n")
                out_f.write(content)
                out_f.write("\n\n")
    print(f"✅ 导出完成！文件：{OUTPUT_FILE}")

if __name__ == "__main__":
    export_project_code()
