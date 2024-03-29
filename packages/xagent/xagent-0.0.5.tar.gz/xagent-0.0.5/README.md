# XAgents

XAgents项目为在大模型服务基础上的中间件，为了避免各个业务线重复开发，提供统一的程序接口，快速支持各种业务的需求

## 主要能力

- 接入各种模型服务，包括zhipu sdk, 本地LLM，embedding模型，rerank模型，NLU模型等
- 知识库的管理
- RAG的能力
- 工具调用的能力

具体设计参考[文档](https://zhipu-ai.feishu.cn/docx/Y78IdJZSmoESK0x0HZpc7vrWnde)

## 接入方式

### python SDK（python程序快速接入）

#### install

基于python3.10以上版本
  `pip install -U xagent`

#### 本地知识库

参考 tutorial/local_kb.py

#### 服务端知识库

参考 tutorial/remote_kb.py

#### http Service

测试环境&内部生产环境: 117.50.174.44:8001

测试代码
  ```shell
curl -X 'POST' \
  'http://localhost:8001/kb/list' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic emhpcHU6emhpcHU=' \
  -d ''
```

具体接口文档参考 http://117.50.174.44:8001/docs
鉴权的用户名和密码都是zhipu


## Release Note

### 20240325

version: 0.0.4

- 创建了工程项目以及[README文档](https://dev.aminer.cn/solution-center-algorithm/XAgents)、[DEVELOP文档](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/blob/main/DEVELOP.md?ref_type=heads)
- 提供知识库的增删改查、搜索、索引接口
- 提供了知识库文件的增删改查、更新、切片接口
- 提供http接口文档:http://117.50.174.44:8001/docs
- 提供python sdk以及调用[教程](https://dev.aminer.cn/solution-center-algorithm/XAgents/-/tree/main/tutorial?ref_type=heads)
