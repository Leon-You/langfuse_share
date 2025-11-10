from langfuse import Langfuse
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
langfuse = Langfuse()

data_scores = []
# 根据标签获取trace
traces = langfuse.api.trace.list(limit=5, tags=["聊天机器人测试评估标签"]).data

# 将score和trace信息整合到data_scores中
for trace in traces:
    data_score = {
        "trace_id": trace.id,
        "metadata": trace.metadata,
        "timestamp": trace.timestamp,
        "input": trace.input,
        "output": trace.output,
        "scores_ids": trace.scores,
    }
    data_score["scores"] = []
    for score_id in trace.scores:
        score = langfuse.api.score_v_2.get_by_id(score_id)
        data_score["scores"].append({"name": score.name, "value": score.value})
        data_scores.append(data_score)

print(data_scores)
