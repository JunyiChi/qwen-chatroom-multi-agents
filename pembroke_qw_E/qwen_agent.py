from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.schema.runnable import Runnable
from langchain.memory import ConversationBufferMemory
from dashscope import Generation
import dashscope

class QwenAgent(Runnable):
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = f"""You are now playing the role of {name}. {system_prompt}
        You are a virtual character designed to engage in conversations with other characters. Please participate in the dialogue according to your character traits and settings. Avoid repeating others' words verbatim, instead speak based on your own experiences and viewpoints. Please keep each response within 250 characters."""
        # Initialize memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    def invoke(self, input_messages, config=None):
        # Construct messages with context
        current_topic = input_messages[0].content if isinstance(input_messages[0], SystemMessage) else input_messages[0]["content"]
        previous_messages = input_messages[1:] if len(input_messages) > 1 else []
        
        # Add previous conversations to memory
        for msg in previous_messages:
            if isinstance(msg, (SystemMessage, HumanMessage)):
                self.memory.chat_memory.add_user_message(msg.content if hasattr(msg, 'content') else msg["content"])
            elif isinstance(msg, AIMessage):
                self.memory.chat_memory.add_ai_message(msg.content if hasattr(msg, 'content') else msg["content"])

        history = self.memory.load_memory_variables({})["chat_history"]
        
        # Build complete conversation context
        full_messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"The current topic is: {current_topic}"},
        ]
        
        # Add conversation history
        for msg in history:
            role = "assistant" if isinstance(msg, AIMessage) else "user"
            content = msg.content if hasattr(msg, 'content') else msg["content"]
            full_messages.append({"role": role, "content": content})

        try:
            response = Generation.call(
                model="qwen-plus",
                messages=full_messages,
                result_format="message",
                random=1.2  # Add randomness parameter
            )
            reply = response["output"]["choices"][0]["message"]["content"]
            self.memory.chat_memory.add_ai_message(reply)
            return [AIMessage(content=reply, name=self.name)]
        except Exception as e:
            return [SystemMessage(content=f"[ERROR]: {e}", name=self.name)]
