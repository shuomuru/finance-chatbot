# 金融问答机器人 (Finance Chatbot)

一个基于自然语言处理和RAG（检索增强生成）技术的智能金融问答系统，支持多轮对话、意图识别和上下文理解。

## 功能特性

### 核心功能
- **智能问答**：基于NLP引擎的意图识别和槽位填充，支持股票、基金、保险、投资建议等多领域问答
- **知识检索**：基于FAISS向量数据库的RAG系统，结合BGE嵌入模型和重排序模型提供精准检索
- **模型对比**：支持基座模型与微调模型的回答效果对比
- **多轮对话**：支持上下文感知的连续对话，自动维护会话状态

### 技术特性
- **意图识别**：基于规则模式的意图分类，支持9种金融相关意图
- **槽位填充**：自动提取股票代码、投资金额、时间范围等关键信息
- **会话管理**：支持会话创建、维护、清理，自动超时处理
- **数据持久化**：SQLite数据库存储会话历史和对话状态

## 技术栈

- **后端框架**：FastAPI + Uvicorn
- **NLP引擎**：自定义意图识别 + Slot Filling
- **向量检索**：FAISS + BGE-Large-Zh-V1.5 嵌入模型
- **重排序**：BGE-Reranker-Base
- **大语言模型**：Qwen2.5-7B-Instruct (通过SiliconFlow API)
- **数据库**：SQLite
- **前端**：原生HTML/CSS/JavaScript

## 项目结构

```
.
├── app.py                 # FastAPI主应用入口
├── models.py              # Pydantic数据模型定义
├── dialogue_manager.py    # 对话管理器
├── nlp_engine.py          # NLP引擎（意图识别、槽位填充、响应生成）
├── prompt.py              # RAG检索和LLM调用模块
├── database.py            # SQLite数据库操作
├── index.html             # 前端聊天界面
├── requirements.txt       # Python依赖
└── faiss_db/              # FAISS向量数据库（需自行创建）
```

## 快速开始

### 环境要求
- Python 3.8+
- 至少 8GB 内存（用于加载模型）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置API密钥

在 `prompt.py` 中配置你的 SiliconFlow API 密钥：

```python
API_KEY = "your-api-key-here"
```

### 准备向量数据库

确保 `faiss_db` 目录存在并包含已构建的FAISS索引文件。如果没有，你需要：
1. 准备金融领域的文档数据
2. 使用 BAAI/bge-large-zh-v1.5 模型生成嵌入向量
3. 构建FAISS索引并保存到 `faiss_db` 目录

### 启动服务

```bash
python app.py
```

服务将在 `http://localhost:8000` 启动。

## API接口

### 智能问答
```http
POST /chat
Content-Type: application/json

{
  "question": "什么是基金？",
  "session_id": "optional-session-id",
  "user_id": "optional-user-id"
}
```

### RAG知识检索
```http
POST /rag-chat
Content-Type: application/json

{
  "question": "股票和基金的区别是什么？"
}
```

### 模型对比
```http
POST /compare
Content-Type: application/json

{
  "question": "如何进行风险评估？"
}
```

### 健康检查
```http
GET /health
```

### 统计数据
```http
GET /statistics
```

### 会话管理
```http
GET /session/{session_id}      # 获取会话信息
DELETE /session/{session_id}   # 清除会话
GET /history/{session_id}      # 获取会话历史
```

## 支持的意图类型

| 意图 | 描述 | 关键词示例 |
|------|------|-----------|
| greeting | 问候 | 你好、您好、hi |
| stock_query | 股票查询 | 股票、股价、A股、大盘 |
| fund_query | 基金查询 | 基金、净值、定投、申购 |
| insurance_query | 保险咨询 | 保险、投保、理赔、医疗险 |
| investment_advice | 投资建议 | 投资、理财、配置、收益 |
| risk_assessment | 风险评估 | 风险、评估、承受能力 |
| account_info | 账户信息 | 账户、余额、密码、登录 |
| complaint | 投诉反馈 | 投诉、不满、问题 |
| goodbye | 结束对话 | 再见、拜拜、谢谢 |

## 前端界面

访问 `http://localhost:8000` 即可使用Web聊天界面，支持：
- 三种模式切换：智能问答 / 知识检索 / 模型对比
- 快速问题快捷按钮
- 会话管理和清除
- 响应式暗色主题设计

## 模型说明

本项目使用以下模型：
- **嵌入模型**：BAAI/bge-large-zh-v1.5
- **重排序模型**：BAAI/bge-reranker-base
- **大语言模型**：Qwen/Qwen2.5-7B-Instruct

模型将通过 HuggingFace 镜像自动下载（首次运行需要较长时间）。

## 开发计划

- [ ] 添加更多金融领域意图类型
- [ ] 集成深度学习意图分类模型
- [ ] 支持语音输入和输出
- [ ] 添加用户认证和权限管理
- [ ] 支持多语言（英文）

## 许可证

MIT License

## 致谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://python.langchain.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [BGE](https://github.com/FlagOpen/FlagEmbedding)
- [Qwen](https://github.com/QwenLM/Qwen)
