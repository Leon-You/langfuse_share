import httpx
from langfuse import get_client, Evaluation
import random
import time
from dotenv import load_dotenv
load_dotenv()

client = get_client()

# 要评估的功能接口
async def task(*, item, **_):
    url = "http://127.0.0.1:8000/chat"
    data = {"message": item.input["user_input"]}
    start_time = time.time()
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
    end_time = time.time()
    return {"output": response.json(), "time": end_time - start_time}

# 回复正确性评估
async def evaluator_1(*, input, output, expected_output, **kwargs):
    if output["output"]['reply'] == expected_output["expected_output"]:
        return Evaluation(name="回复正确性", value=1)
    else:
        return Evaluation(name="回复正确性", value=0)

# 模拟多个时间点评估
async def evaluator_2(*, input, output, expected_output, **kwargs):
    time_1 = random.random()
    return [
        Evaluation(name="回复时间", value=output["time"]),
        Evaluation(name="回复时间-fake", value=time_1),
    ]

# 整体评估
async def overall_evaluator(*, item_results, **kwargs):
    time_list = [
        eval.value for result in item_results
        for eval in result.evaluations if eval.name == "回复时间"
    ]
    time_fake_list = [
        eval.value for result in item_results
        for eval in result.evaluations if eval.name == "回复时间-fake"
    ]
    time_max = max(time_list)
    time_fake_max = max(time_fake_list)
    return [
        Evaluation(name="回复时间最大值", value=time_max),
        Evaluation(name="回复时间-fake最大值", value=time_fake_max),
    ]

def main():
    dataset = client.get_dataset("聊天机器人测试集")
    result = dataset.run_experiment(
        name="聊天机器人测试评估结果",
        task=task,
        evaluators=[evaluator_1, evaluator_2],
        run_evaluators=[overall_evaluator],
        metadata={
            "langfuse_tags": ["聊天机器人测试评估标签"], # 用于在langfuse中搜索该评估结果，用在9_post_analysis.py中
        },
        max_concurrency = 2
    )
    print(result.format())

if __name__ == "__main__":
    main()