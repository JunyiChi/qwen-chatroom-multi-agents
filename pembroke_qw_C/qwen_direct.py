import dashscope

dashscope.api_key = "sk-cf9b5fd942224ebf9b88943331fa7e84"  # 这里填你自己的

from dashscope import Generation

response = Generation.call(
    model="qwen-max",  # 你也可以试试 "qwen-turbo" 或 "qwen-max"
    messages=[
        {"role": "system", "content": "你是一个非常宜人（agreeable）的员工，尽量缓和冲突，支持别人。"},
        {"role": "user", "content": "你觉得应该实行每周一天的远程办公吗？"}
    ],
    result_format="message"  # 返回格式设为 message 类型，结构与 OpenAI 一致
)

print(response['output']['choices'][0]['message']['content'])