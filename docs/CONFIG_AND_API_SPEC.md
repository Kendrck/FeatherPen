# FeatherPen/docs/CONFIG_AND_API_SPEC.md
# GB/T 8567 全局配置与通信端口国标规范
## 一、配置加载优先级（从低到高）
1. 代码内置默认值
2. config.yaml本地配置文件
3. 系统环境变量 FP_NETWORK_PREFERRED_PORT（最高优先级）

## 二、config.yaml固定端口配置节点
network:
  bind_address: "127.0.0.1"
  preferred_port: 6554
llm:
  local_api_port: 1234
约束：禁止在代码中直接写死6554/1234数字，统一由config_loader读取

## 三、环境变量规则
环境变量名称：FP_NETWORK_PREFERRED_PORT
仅覆盖Web服务端口，LLM推理端口不受环境变量控制
值必须1024~65535整数，非法自动回落1234

## 四、端口容错完整规范
1. 启动绑定端口捕获OSError占用异常
2. 自动遍历分配本机空闲端口
3. 控制台打印当前实际监听端口，前端/api/status同步返回

## 五、HTTP通信统一规则
1. 基准URL前缀：http://127.0.0.1:{web_port}/api/v1
2. 所有接口统一JSON返回结构，错误码全局统一
3. 前端禁止拼接硬编码地址，调用/status动态获取端口
4. LLM推理固定地址模板 http://127.0.0.1:{llm.local_api_port}/v1/chat/completions

## 六、配置加载标准函数
统一使用src/config/config_loader内load_global_config()
废弃旧名称load_config，全项目禁止调用

## 七、配置缺失兜底机制
init_env.py检测无config.yaml时，自动写入标准6554/1234、127.0.0.1配置模板