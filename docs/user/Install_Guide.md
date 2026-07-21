# FeatherPen 安装部署指南 V1.0
## 环境依赖
Python 3.10+

## 快速安装步骤
1. 克隆项目至本地
2. 运行 scripts/user/setup.bat 自动部署依赖
3. 执行根目录 main.py 启动程序

## 手动安装
```
pip install -r requirements.txt
```

## 启动方式
- 命令行：python main.py
- 双击 main.py 直接启动

## 目录自动初始化规则
程序首次启动自动创建：
- data/ 运行数据目录
- logs/ 日志目录
- 自动复制默认配置 app.default.ini 生成本地 app.ini

## 安装异常处理
- 依赖安装失败：手动更新pip后重试
- 配置缺失：程序自动重置默认配置
- 目录权限不足：切换普通用户权限运行
