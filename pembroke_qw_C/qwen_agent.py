from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.schema.runnable import Runnable
from langchain.memory import ConversationBufferMemory
from dashscope import Generation
import dashscope

class QwenAgent(Runnable):
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = f"""你现在扮演{name}。{system_prompt}
        你是一个虚拟角色，旨在与其他角色进行对话。请根据你的角色特点和设定，参与到对话中去。避免重复他人的原话,而是基于自己的经历和观点来发言。请每次发言控制在250个字以内。"""
        # 初始化记忆
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def invoke(self, input_messages, config=None):
        # 构建包含上下文的消息
        current_topic = input_messages[0].content if isinstance(input_messages[0], SystemMessage) else input_messages[0]["content"]
        previous_messages = input_messages[1:] if len(input_messages) > 1 else []
        
        # 将之前的对话添加到记忆中
        for msg in previous_messages:
            if isinstance(msg, (SystemMessage, HumanMessage)):
                self.memory.chat_memory.add_user_message(msg.content if hasattr(msg, 'content') else msg["content"])
            elif isinstance(msg, AIMessage):
                self.memory.chat_memory.add_ai_message(msg.content if hasattr(msg, 'content') else msg["content"])

        history = self.memory.load_memory_variables({})["chat_history"]
        
        # 构建完整的对话上下文
        full_messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"当前讨论的话题是：{current_topic}"},
        ]
        
        # 添加历史对话记录
        for msg in history:
            role = "assistant" if isinstance(msg, AIMessage) else "user"
            content = msg.content if hasattr(msg, 'content') else msg["content"]
            full_messages.append({"role": role, "content": content})

        try:
            response = Generation.call(
                model="qwen-plus",
                messages=full_messages,
                result_format="message",
                random=1.2  # 添加随机性参数
            )
            reply = response["output"]["choices"][0]["message"]["content"]
            self.memory.chat_memory.add_ai_message(reply)
            return [AIMessage(content=reply, name=self.name)]
        except Exception as e:
            return [SystemMessage(content=f"[ERROR]: {e}", name=self.name)]
