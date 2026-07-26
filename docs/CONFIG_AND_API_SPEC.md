# FeatherPen/docs/CONFIG_AND_API_SPEC.md
# GB/T 8567 全局配置与通信端口国标规范
## 一、配置加载优先级（由低至高）
1. 代码内置默认参数
2. 本地config.yaml配置文件
3. 系统环境变量 FP_NETWORK_PREFERRED_PORT（最高优先级，仅覆盖Web端口）
## 二、config.yaml标准端口节点
network:
  bind_address: "127.0.0.1"
  preferred_port: 6554
llm:
  local_api_port: 1234
强制约束：代码禁止直接写死6554/1234数字，统一调用config_loader读取
## 三、环境变量使用规则
变量名称：FP_NETWORK_PREFERRED_PORT
仅控制Web后台端口；llm.local_api_port固定1234不受环境变量影响
合法区间1024~65535，非法数值自动回落默认1234
## 四、端口容错分层强制规范
1. Web端口6554：程序启动捕获OSError端口占用异常，自动遍历本机空闲端口；
2. LLM推理端口1234：固定配置，不存在自动分配逻辑，占用需手动结束对应进程释放；
3. 控制台打印最终生效Web端口，前端页面初始化同步拉取接口真实端口。
## 五、HTTP通信统一标准
1. 全局基准URL模板：http://127.0.0.1:{web_port}/api/v1
2. 全部接口统一JSON返回结构、全局错误码
3. 前端禁止拼接固定端口地址，页面初始化动态拉取
4. LLM推理固定请求地址：http://127.0.0.1:{llm.local_api_port}/v1/chat/completions
## 六、标准配置读取函数
全局统一使用load_global_config()；废弃旧函数load_config，全项目禁用
## 七、配置缺失兜底机制
init_env.py检测无config.yaml文件时，自动写入6554/1234、127.0.0.1标准配置模板