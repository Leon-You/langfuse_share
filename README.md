# Langfuse 使用示例代码

这个仓库包含 Langfuse 的完整使用示例，演示如何在实际项目中集成 Langfuse 进行 LLM 应用的可观测性监控、追踪和评估。

## 项目结构

```
langfuse_share/
├── app/                        # FastAPI 聊天机器人应用
│   ├── main.py                # 主应用代码（包含 Langfuse 集成示例）
│   ├── requirements.txt       # 应用依赖
│   └── run.sh                 # 启动脚本
├── eval/                       # 评估相关脚本
│   ├── 1_prepare_data.py      # 准备测试数据集
│   ├── 2_run_eval.py          # 运行评估实验
│   └── 9_post_analysis.py     # 后处理与数据分析
├── .env.example               # 环境变量配置示例
└── README.md
```

## 快速开始

### 1. 环境配置

复制环境变量配置文件并填写你的 Langfuse 配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 Langfuse 配置信息：

```bash
LANGFUSE_HOST=http://your-langfuse-host:port
LANGFUSE_PUBLIC_KEY=pk-lf-xxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxx
```

### 2. 安装依赖

```bash
cd app
pip install -r requirements.txt
```

### 3. 运行聊天机器人应用

```bash
# 使用启动脚本
bash run.sh

# 或直接使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

应用启动后，访问 http://localhost:8000/docs 查看 API 文档。

### 4. 测试 API

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "message": "你好"}'
```

## 功能模块详解

### 一、聊天机器人应用 (`app/main.py`)

这是一个集成了 Langfuse 的 FastAPI 应用，展示了以下核心功能：

#### 1. 自动追踪 (`@observe`)
使用 `@observe` 装饰器自动追踪函数执行：

```python
@observe(name="聊天机器人")
async def chatbot(message: str):
    # 函数执行会自动记录到 Langfuse
    ...
```

#### 2. 用户属性传播 (`propagate_attributes`)
关联用户 ID 到所有追踪数据：

```python
@observe(name="聊天机器人包装器")
async def chatbot_wrapper(user_id: str, message: str):
    with propagate_attributes(user_id=user_id):
        return await chatbot(message)
```

#### 3. 手动创建 Span
追踪内部处理逻辑的执行时间和输出：

```python
span = client.start_span(name="第一个span")
# ... 执行业务逻辑 ...
span.update(output=f"处理结果: {result}")
span.end()
```

#### 4. Generation 追踪
专门用于记录 LLM 生成过程：

```python
generation = client.start_generation(
    name="模型生成",
    model="xx-model",
    input=[{"role": "user", "content": message}]
)
# ... 模型推理 ...
generation.update(output=[{"role": "assistant", "content": reply}])
generation.end()
```

### 二、评估流程 (`eval/`)

完整的评估流程包含三个步骤：

#### 步骤 1: 准备测试数据 (`1_prepare_data.py`)

创建测试数据集并上传到 Langfuse：

```bash
python eval/1_prepare_data.py
```

功能：
- 创建名为 "聊天机器人测试集" 的数据集
- 批量上传测试样本（包含输入和预期输出）

#### 步骤 2: 运行评估实验 (`2_run_eval.py`)

执行自动化评估：

```bash
python eval/2_run_eval.py
```

功能：
- 调用待测试的 API 接口
- 执行多个评估器：
  - **回复正确性评估**：对比实际输出与预期输出
  - **性能指标评估**：模拟响应时间等指标
  - **整体评估**：汇总所有测试项的评估结果
- 支持并发执行（`max_concurrency=2`）
- 结果自动上传到 Langfuse

#### 步骤 3: 后处理分析 (`9_post_analysis.py`)

提取和分析评估结果：

```bash
python eval/9_post_analysis.py
```

功能：
- 使用标签从 Langfuse 检索评估数据
- 整合 trace 和 score 信息
- 便于后续进行数据分析和可视化

## 核心概念

### Langfuse 关键组件

1. **Trace（追踪）**：完整请求的执行链路
2. **Span（跨度）**：请求中的单个操作或步骤
3. **Generation（生成）**：专门用于 LLM 调用的特殊 Span
4. **Score（评分）**：对 Trace 或 Generation 的评估结果
5. **Dataset（数据集）**：用于评估的测试数据集合

### 工作流程

```
用户请求 → FastAPI 接口 → Langfuse 自动追踪
    ↓
  记录 Trace
    ↓
  创建 Span（内部处理）
    ↓
  创建 Generation（模型生成）
    ↓
  返回响应 + 上传追踪数据到 Langfuse
```

## 适用场景

- LLM 应用性能监控
- 对话质量评估
- A/B 测试对比
- 模型版本管理
- 用户行为分析
- 自动化测试与回归测试

## 依赖项

主要依赖包：
- `fastapi` - Web 框架
- `langfuse` - 可观测性 SDK
- `pydantic` - 数据验证
- `python-dotenv` - 环境变量管理
- `httpx` - HTTP 客户端（用于评估）
- `tqdm` - 进度条显示

## 注意事项

1. 确保 Langfuse 服务已启动并可访问
2. 配置文件 `.env` 不要提交到版本控制系统
3. 评估实验会生成大量追踪数据，注意存储空间
4. 并发评估时注意 API 速率限制

## 参考资源

- [Langfuse 官方文档](https://langfuse.com/docs)
- [Langfuse Python SDK](https://github.com/langfuse/langfuse-python)
- [FastAPI 文档](https://fastapi.tiangolo.com/)

## License

本项目仅用于学习和示例演示。