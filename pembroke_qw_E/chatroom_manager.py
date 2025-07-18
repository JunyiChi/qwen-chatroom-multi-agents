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
        self.current_speaker = None  # Add tracking for the current speaker
    
def extract_respond_to(self, text: str) -> list:
    names = list(self.agents.keys())
    mentioned_names = []

    # 1. Strong signal: @ mark or direct name mention
    matches = re.findall(r"@([\w\u4e00-\u9fff]+)", text)
    mentioned_names.extend([name for name in matches if name in names])

    # 1.1 Strong signal supplement: direct address at the beginning, like "Max, what do you think"
    for name in names:
        # Match beginning address (allowing punctuation and spaces)
        if re.match(rf"^\s*{name}[，,:：]", text) and name != self.current_speaker:
            mentioned_names.append(name)

    # Remove duplicates (might be matched by both @ and beginning address)
    mentioned_names = list(set(mentioned_names))

    # 2. Medium signal: name mentioned in full text (excluding beginning)
    if not mentioned_names:
        for name in names:
            if name in text and name != self.current_speaker:
                mentioned_names.append(name)

    # 3. Weak signal: default to responding to the previous speaker
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
                
                # Use structured memory to build context
                memory_context = self.memory_manager.select_memories(speaker, max_others=10)
                current_input = memory_context + "\n\nCurrent topic is: " + self.topic

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

                # Add the speech to the structured memory pool
                self.memory_manager.add_memory(speaker, output.content)

        print("\n🔷 Conversation ended")

    def save_to_json(self, filename="chat_log.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.chat_log, f, indent=2, ensure_ascii=False)
