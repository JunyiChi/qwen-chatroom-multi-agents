# memory_manager.py
import time
from collections import defaultdict
from typing import List, Dict

class MemoryManager:
    def __init__(self):
        # Internal structure: each agent has their own set of memories
        self.memory_pool: Dict[str, List[dict]] = defaultdict(list)

    def add_memory(self, speaker: str, text: str):
        """
        Record a new message as a memory entry.
        Each memory includes: speaker, text, timestamp.
        """
        memory = {
            "speaker": speaker,
            "text": text,
            "timestamp": time.time()
        }
        self.memory_pool[speaker].append(memory)

    def select_memories(self, agent_name: str, max_others: int = 10) -> str:
        """
        Retrieve all memories of the current agent + the most recent max_others memories from others.
        Return a concatenated natural language context string.
        """
        own_memories = self.memory_pool[agent_name]  # All own memories
        others_memories = []

        for name, mems in self.memory_pool.items():
            if name != agent_name:
                others_memories.extend(mems)

        # Sort by timestamp and get the most recent max_others
        others_memories = sorted(others_memories, key=lambda m: -m["timestamp"])[:max_others]

        # Concatenate context text
        memory_lines = []
        if own_memories:
            memory_lines.append(f"Your past experiences:")
            for mem in own_memories:
                memory_lines.append(f"- You once said: {mem['text']}")

        if others_memories:
            memory_lines.append("Related messages from others:")
            for mem in others_memories:
                memory_lines.append(f"- {mem['speaker']} once said: {mem['text']}")

        return "\n".join(memory_lines)

    def get_all_memories(self) -> dict:
        """
        Retrieve the complete memory_pool content (for analysis or saving).
        """
        return self.memory_pool
