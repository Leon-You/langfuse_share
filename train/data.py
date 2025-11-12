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
    datasets.append({
        "input": d.input,
        "output": d.output,
    })

print(datasets)