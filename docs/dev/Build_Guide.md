# FeatherPen/docs/dev/Build_Guide.md
# GB/T 8567 V1.0.0 打包发布开发规范
## 一、打包工具统一使用PyInstaller
## 二、前置校验规则
打包执行前必须：
1. 完整执行pytest单元测试，无报错
2. 更新CHANGELOG.md版本变更记录
3. 清理runtime缓存、logs日志、dist旧产物
4. 核对STRUCTURE.md与物理文件完全一致

## 三、产物输出目录
打包产物统一输出至 FeatherPen/dist，.gitignore自动屏蔽dist目录不提交代码仓库
Windows双产物：Setup安装包 + 便携绿色zip包
macOS：dmg镜像
Linux：AppImage / deb / rpm
拓展产物（V2规划）：Web Docker、Android APK、VSCode插件

## 四、打包脚本文件
Windows：build.bat、setup.bat，源码根目录直接运行
打包过滤规则：自动过滤tests测试目录、dev开发文档草稿、runtime临时文件

## 五、发布交付标准
1. 交付包附带完整归档文档（STRUCTURE.md、API_MODULE_SPEC.md、用户手册）
2. 打包内置默认端口6554，不修改config.yaml国标默认配置
3. 永久移除ui/electron打包分支，不生成旧界面安装包