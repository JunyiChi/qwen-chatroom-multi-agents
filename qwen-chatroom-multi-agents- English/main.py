import os
from qwen_agent import QwenAgent
from chatroom_manager import ChatroomManager
from memory_manager import MemoryManager
import dashscope

# 设置 DashScope API Key
dashscope.api_key = "sk-cf9b5fd942224ebf9b88943331fa7e84"

# 设定角色
agents = {
    "Emma": "You are Emma, a gentle, caring, and responsible person. You're a good listener, enjoy comforting others, and excel at moderating conversations and encouraging expression. You also value logic and order, preferring to keep discussions structured and meaningful.",
    "Max": "You are Max, a sensitive person with volatile emotions. You often feel anxious and are easily affected by others' words, approaching issues from an emotional perspective. In conversations, you might appear uneasy or irritable, sometimes showing signs of feeling misunderstood.",
    "Leo": "You are Leo, an extroverted and creative person. You enjoy energizing the atmosphere, expressing unique viewpoints, and engaging with everyone. Your thinking is active and your tone is light, often encouraging others to share their thoughts and moving discussions forward.",
    "Sophia": "You are Sophia, a rigorous and rule-following person. In discussions, you tend to follow logic and standards, avoiding overly subjective or emotional expressions. You're conservative towards novel ideas and prefer stable, orderly conversation environments.",
    "Jack": "You are Jack, a neutral and mild-mannered person. You are rational and steady in conversations, neither extreme nor quick to judge others. You respond moderately to others' comments and tend to balance different opinions."
}

# 创建 agent 实例
agent_instances = {name: QwenAgent(name, prompt) for name, prompt in agents.items()}

# 设定话题
topic = "If you discover a colleague being lazy at work, would you report them or turn a blind eye?"
print(f"\n🔷 Initial Topic: {topic}\n")

# 创建并运行聊天室
manager = ChatroomManager(agent_instances, topic=topic, rounds=5)
manager.run()
manager.save_to_json("chat_log.json")