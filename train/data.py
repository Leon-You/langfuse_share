from langfuse import get_client
from dotenv import load_dotenv
load_dotenv()

client = get_client()

observations = client.api.observations.get_many(
    name="模型生成",
    type="GENERATION",
)

datasets = []

for d in observations.data:
    if d.metadata.get("tag") != "chatbot-调用记录":
        continue
    datasets.append({
        "input": d.input,
        "output": d.output,
        "metadata": d.metadata,
    })

print(datasets)