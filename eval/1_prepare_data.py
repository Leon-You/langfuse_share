from langfuse import get_client
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

client = get_client()
# 测试数据示例
data = [
    {"user_input": "你好吗？", "expected_output": "你好呀，我是你的虚拟助手 😊"},
    {"user_input": "今天天气怎么样？", "expected_output": "今天天气很好，适合写代码。"},
    {"user_input": "你是谁？", "expected_output": "我是你的虚拟助手 😊"},
    {"user_input": "你是谁？", "expected_output": "我是你的虚拟助手 😊"},
]

def prepare_data():

    dataset_name = "聊天机器人测试集"
    # 创建数据集
    client.create_dataset(
        name=dataset_name,
        description="聊天机器人测试集",
        metadata={
            "module": "聊天机器人",
        }
    )
    # 写入数据集
    for item in tqdm(data):
        client.create_dataset_item(
            dataset_name=dataset_name,
            input={"user_input": item["user_input"]},
            expected_output={"expected_output": item["expected_output"]},
        )

if __name__ == "__main__":
    prepare_data()