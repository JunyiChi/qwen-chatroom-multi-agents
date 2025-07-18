# memory_manager.py
import time
from collections import defaultdict
from typing import List, Dict

class MemoryManager:
    def __init__(self):
        # 内部结构：每个 agent 拥有一组自己的记忆
        self.memory_pool: Dict[str, List[dict]] = defaultdict(list)

    def add_memory(self, speaker: str, text: str):
        """
        将一条新的发言记录为 memory 条目。
        每条 memory 结构包括：speaker, text, timestamp。
        """
        memory = {
            "speaker": speaker,
            "text": text,
            "timestamp": time.time()
        }
        self.memory_pool[speaker].append(memory)

    def select_memories(self, agent_name: str, max_others: int = 10) -> str:
        """
        获取当前 agent 所有自己的记忆 + 最近 max_others 条他人的记忆。
        返回一个拼接好的自然语言上下文字符串。
        """
        own_memories = self.memory_pool[agent_name]  # 自己的所有记忆
        others_memories = []

        for name, mems in self.memory_pool.items():
            if name != agent_name:
                others_memories.extend(mems)

        # 根据时间戳排序，获取最近的 max_others 条
        others_memories = sorted(others_memories, key=lambda m: -m["timestamp"])[:max_others]

        # 拼接上下文文本
        memory_lines = []
        if own_memories:
            memory_lines.append(f"你的过往经历：")
            for mem in own_memories:
                memory_lines.append(f"- 你曾说过：{mem['text']}")

        if others_memories:
            memory_lines.append("其他人的相关发言：")
            for mem in others_memories:
                memory_lines.append(f"- {mem['speaker']} 曾说过：{mem['text']}")

        return "\n".join(memory_lines)

    def get_all_memories(self) -> dict:
        """
        获取完整 memory_pool 内容（用于分析或保存）。
        """
        return self.memory_pool
