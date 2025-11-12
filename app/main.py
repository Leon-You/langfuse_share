# ------------------------ FastAPI 逻辑 ------------------------

from fastapi import FastAPI
from pydantic import BaseModel, Field

# 定义请求体模型
class ChatRequest(BaseModel):
    user_id: str = Field(default="test_user_id", description="用户ID")
    message: str = Field(default="你好", description="用户消息")

# 定义响应体模型
class ChatResponse(BaseModel):
    reply: str = Field(..., description="机器人回复")

# 创建 FastAPI 应用
app = FastAPI(title="Simple Chatbot API", description="一个简单的对话机器人接口示例")

# 定义一个 POST 接口
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    一个简单的聊天机器人接口。
    """
    reply = await chatbot_wrapper(request.user_id, request.message)
    
    return ChatResponse(reply=reply)

# ------------------------ 聊天机器人逻辑 ------------------------
from langfuse.openai import openai
from langfuse import observe, get_client, propagate_attributes
from dotenv import load_dotenv
import time
# 加载langfuse需要的环境变量
load_dotenv("../.env")
# 获取Langfuse客户端
client = get_client()

@observe(name="聊天机器人包装器")
async def chatbot_wrapper(user_id: str, message: str):
    with propagate_attributes(user_id=user_id):
        return await chatbot(message)

@observe(name="聊天机器人")
async def chatbot(message: str):
    """
    模拟一个简单的聊天机器人回复。
    """
    # 创建一个内部span，用于记录内部处理时间
    span = client.start_span(name="第一个span")
    time.sleep(0.3) # 模拟内部处理时间
    span.update(output=f"第一个span处理完成: {message}")
    span.end()

    # 创建一个生成span，用于记录生成过程（Python SDK）
    generation = client.start_generation(
                name="模型生成",
                model="xx-model",
                input=[
                    {"role": "system", "content": "你是一个虚拟助手，请根据用户的问题给出回答。"},
                    {"role": "user", "content": message}
                    ],
                metadata={"tag": "chatbot-调用记录"},
            )
    time.sleep(0.5) # 模拟生成时间
    if "你好" in message:
        reply = "你好呀，我是你的虚拟助手 😊"
    elif "天气" in message:
        reply = "今天天气很好，适合写代码。"
    else:
        reply = f"你说的是：{message}？这个我还不太懂～"
    generation.update(output=[{"role": "assistant", "content": reply}])
    generation.end()

    # 创建一个生成span，用于记录生成过程（OpenAI SDK）
    # completion = openai.chat.completions.create(
    #     name="模型生成",
    #     model="xx-model",
    #     messages=[
    #         {"role": "system", "content": "你是一个虚拟助手，请根据用户的问题给出回答。"},
    #         {"role": "user", "content": message}],
    # )
    # reply = completion.choices[0].message.content
    # 刷新所有span
    client.flush()
    return reply
