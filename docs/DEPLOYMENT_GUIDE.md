# FeatherPen/docs/DEPLOYMENT_GUIDE.md
# GB/T 8567 V1.0.0 全平台打包部署规范
## 一、环境最低要求
Python3.10+，内存≥4G，磁盘空闲≥2G
## 二、本地源码部署流程
1. 拉取完整项目源码
2. 根目录执行 python init_env.py 初始化依赖与目录
3. python main.py 启动桌面客户端

## 三、Windows打包（build.bat）
1. 自动清理runtime缓存、旧日志
2. PyInstaller打包单文件便携版 + exe安装包
3. 产物输出dist目录：
FeatherPen_V1.0.0_Windows_Setup.exe / FeatherPen_V1.0.0_Windows_Portable.zip
4. 打包自动过滤dist、runtime/logs临时文件

## 四、macOS打包流程
执行对应打包脚本生成dmg镜像，适配mac沙盒本地文件读写

## 五、Linux打包产物
AppImage、deb、rpm三种分发包，适配主流发行版

## 六、Web/插件拓展产物（预留V2.0）
dist内Docker网页包、安卓APK、Chrome插件、VSCode插件仅规划，V1.0不交付

## 七、打包硬性约束
1. 打包产物仅包含离线本地逻辑，无云端接口代码
2. 自动删除ui/electron废弃目录打包分支
3. 内置端口配置固定6554/1234，打包不修改默认值
4. 打包产物不含测试用例tests目录，精简分发体积