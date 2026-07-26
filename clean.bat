:: FeatherPen/clean.bat
:: GB/T 8567 标准化一键清理脚本
:: 基准文档：STRUCTURE.md、API_MODULE_SPEC.md
:: 功能：一键删除虚拟环境、打包产物、Python编译缓存、临时草稿
@echo off
chcp 65001 >nul
echo ========== FeatherPen V1.0.0 标准化清理 ==========
if exist ".venv" (
    rmdir /s /q ".venv"
    echo [完成] 已移除虚拟环境
)
del /f /q *.spec 2>nul
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
del /f /q crash_error.log all_code.txt temp_dedup.py 2>nul
for /r %%d in (__pycache__) do rmdir /s /q "%%d" 2>nul
for /r %%f in (*.pyc *.pyo) do del /f /q "%%f"
if exist runtime\cache rmdir /s /q runtime\cache
if exist runtime\temp rmdir /s /q runtime\temp
echo.
echo ========== 全部标准化清理完成 ==========
pause