# chat_manager.py
import re
import json
import time
from memory_manager import MemoryManager

class ChatroomManager:
    def __init__(self, agents: dict, topic: str, rounds: int = 5):
        self.agents = agents
        self.topic = topic
        self.rounds = rounds
        self.chat_log = []
        self.memory_manager = MemoryManager()
        self.current_speaker = None  # 添加当前发言者追踪
    
def extract_respond_to(self, text: str) -> list:
    names = list(self.agents.keys())
    mentioned_names = []

    # 1. 强信号：@标记 或 名字直接称呼
    matches = re.findall(r"@([\w\u4e00-\u9fff]+)", text)
    mentioned_names.extend([name for name in matches if name in names])

    # 1.1 强信号补充：开头直接称呼，如 "Max，你怎么看"
    for name in names:
        # 匹配开头称呼（允许有标点空格）
        if re.match(rf"^\s*{name}[，,:：]", text) and name != self.current_speaker:
            mentioned_names.append(name)

    # 去重（可能 @ 和开头同时命中）
    mentioned_names = list(set(mentioned_names))

    # 2. 中信号：全文中提到名字（不含开头）
    if not mentioned_names:
        for name in names:
            if name in text and name != self.current_speaker:
                mentioned_names.append(name)

    # 3. 弱信号：默认回应上一发言者
    if not mentioned_names and self.chat_log:
        last_speaker = self.chat_log[-1]["speaker"]
        if last_speaker != self.current_speaker:
            mentioned_names.append(last_speaker)

    return mentioned_names or ["topic"]


    def run(self):
        speakers = list(self.agents.keys())
        
        for round_num in range(self.rounds):
            print(f"\n----- Round {round_num + 1} -----")
            
            for speaker in speakers:
                self.current_speaker = speaker
                agent = self.agents[speaker]
                
                # 使用结构化记忆拼接上下文
                memory_context = self.memory_manager.select_memories(speaker, max_others=10)
                current_input = memory_context + "\n\n当前话题是：" + self.topic

                input_messages = [{"type": "system", "content": current_input}]
                output = agent.invoke(input_messages)[0]

                print(f"{speaker}: {output.content}\n")

                respond_to = self.extract_respond_to(output.content)
                self.chat_log.append({
                    "round": round_num + 1,
                    "speaker": speaker,
                    "respond_to": respond_to,
                    "text": output.content
                })

                # 将发言加入结构化记忆池
                self.memory_manager.add_memory(speaker, output.content)

        print("\n🔷 对话结束")

    def save_to_json(self, filename="chat_log.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.chat_log, f, indent=2, ensure_ascii=False)
