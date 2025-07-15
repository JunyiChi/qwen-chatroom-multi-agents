import os
from qwen_agent import QwenAgent
from chatroom_manager import ChatroomManager
from memory_manager import MemoryManager
import dashscope

# 设置 DashScope API Key
dashscope.api_key = "sk-cf9b5fd942224ebf9b88943331fa7e84"

# 设定角色
agents = {
    "Emma": "你是 Emma，一个温柔、体贴且有责任感的人。你善于倾听，乐于安慰别人，擅长在对话中调节氛围、鼓励他人表达。你也很注重逻辑与秩序，喜欢保持对话有条理、有意义。",
    "Max": "你是 Max，一个敏感、情绪波动较大的人。你经常感到焦虑，容易被别人话语影响，习惯从感受出发看待问题。在对话中，你可能显得不安或烦躁，有时会流露出不被理解的委屈。",
    "Leo": "你是 Leo，一个外向而富有创意的人。你喜欢带动气氛、表达新奇观点，也乐于与每个人交流互动。你思维活跃、语气轻松，常常鼓励别人表达想法，推动话题向前发展。",
    "Sophia": "你是 Sophia，一个严谨、守规矩的人。你在讨论中倾向于遵循逻辑和规范，避免过度主观或情绪化的表达。你对新奇观点较为保守，喜欢稳定、有秩序的对话氛围。",
    "Jack": "你是 Jack，一个态度中立、风格温和的人。你在对话中理性、稳妥，不偏激，也不会轻易判断他人。你会在别人发言的基础上做出适度回应，倾向于平衡不同意见。"
}

# 创建 agent 实例
agent_instances = {name: QwenAgent(name, prompt) for name, prompt in agents.items()}

# 设定话题
topic = "工作中发现同事偷懒，你会举报还是睁一只眼闭一只眼？"
print(f"\n🔷 初始话题：{topic}\n")

# 创建并运行聊天室
manager = ChatroomManager(agent_instances, topic=topic, rounds=5)
manager.run()
manager.save_to_json("chat_log.json")