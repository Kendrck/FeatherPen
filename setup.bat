@echo off
:: 设置控制台编码为UTF-8，解决中文乱码
chcp 65001 >nul
:: 关闭命令回显，只打印自定义输出
@echo off
:: ====================== FeatherPen 羽笔 依赖一键安装脚本 ======================
:: 功能：自动校验Python环境、国内镜像加速安装依赖、安装结果判断、窗口停留不闪退
:: 作者：Kendrck
:: 版本：1.0.1
:: ==============================================================================
echo ====================== FeatherPen 依赖一键安装 ======================
echo 正在校验本机Python环境...
:: 优先使用py启动器（Windows官方Python启动器，多版本共存兼容）
py --version >nul 2>&1 || (
    echo [ERROR] 未检测到Python，请先安装Python并勾选【Add Python to PATH】添加环境变量！
    echo 下载地址：https://www.python.org/downloads/windows/
    pause
    :: 退出脚本，返回错误码1标识执行失败
    exit /b 1
)
echo [INFO] Python环境校验通过，开始安装依赖（清华国内镜像加速）
:: --user 参数：安装至用户目录，避免管理员权限不足报错
:: -i 指定清华PyPI镜像，解决国内下载超时、断连问题
py -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
:: 判断上一条命令执行返回码，0=成功，非0=失败
if %errorlevel% equ 0 (
    echo ==============================================
    echo [SUCCESS] 全部依赖安装完成！
    echo 使用方法：双击 main.py 启动羽毛笔小说工具
    echo ==============================================
) else (
    echo ==============================================
    echo [ERROR] 依赖安装失败，请检查：
    echo 1. 网络是否通畅，可切换手机热点重试
    echo 2. Python版本建议3.10~3.12
    echo 3. 手动执行 py -m pip install --upgrade pip 更新pip
    echo ==============================================
)
:: 执行完毕暂停窗口，防止双击运行后直接闪退，方便查看日志
pause
