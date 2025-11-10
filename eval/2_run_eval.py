import httpx
from langfuse import get_client, Evaluation
from dotenv import load_dotenv
load_dotenv()

client = get_client()

# 要评估的功能接口
async def task(*, item, **_):
    return item.input["user_input"]

async def evaluator_1(*, input, output, expected_output):
    return Evaluation(name="Correctness", value=1)

async def evaluator_2(*, input, output, expected_output):
    return Evaluation(name="Correctness", value=1)

async def overall_evaluator(*, input, output, expected_output):
    return Evaluation(name="Overall", value=1)

def main():
    dataset = client.get_dataset("聊天机器人测试集")
    result = dataset.run_experiment(
        name="聊天机器人测试评估结果",
        task=task,
        evaluators=[evaluator_1, evaluator_2],
        run_evaluators=[overall_evaluator],
        metadata={
            "langfuse_tags": ["聊天机器人测试评估标签"],
        },
        max_concurrency = 2
    )
    print(result.format())

if __name__ == "__main__":
    main()