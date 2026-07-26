# FeatherPen/docs/COMPATIBILITY.md
# GB/T 8567 V1.0.0 全平台兼容国标规范
## 一、支持操作系统清单
Windows10/11、macOS 12+、Linux Ubuntu/Debian/CentOS
## 二、全平台统一强制规则
1. 网络绑定统一127.0.0.1，各平台无外网开放分支代码
2. 端口读取逻辑完全一致，6554/1234默认，冲突自动分配空闲端口
3. 账号校验正则、Lv0-Lv9权限全平台无差异化代码
4. SQLite数据库文件格式跨平台通用，无系统特殊编码
5. PyWebView桌面窗口尺寸、页面交互统一，各平台UI无分支逻辑
6. 目录创建逻辑统一：data/Book四级小说目录、runtime日志目录全平台一致

## 三、平台差异化仅允许内容
1. Windows：build.bat一键打包脚本，exe安装包/便携zip产物
2. macOS：dmg镜像打包，沙盒文件读写权限适配
3. Linux：AppImage/deb/rpm，系统Python路径适配
4. 日志换行符自动适配系统，其余业务逻辑完全统一

## 四、禁止平台差异化开发内容
1. 禁止Windows专属硬件采集、注册表读取逻辑
2. 禁止mac/Linux特殊账号、云端登录分支
3. 禁止各平台独立端口、账号校验规则
4. 禁止Electron/PyQt6分平台界面代码（已全部废弃）

## 五、跨端打包统一标准
dist目录产物命名统一模板：FeatherPen_V1.0.0_系统.后缀
所有平台打包仅过滤缓存日志，不修改业务代码、端口、账号逻辑